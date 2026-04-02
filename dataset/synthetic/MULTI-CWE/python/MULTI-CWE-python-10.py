import os
import ssl
import json
import socket
from pathlib import Path
from datetime import datetime
from typing import Iterable, Dict, List, Optional


EXPORT_ROOT = Path("/srv/billing_exports").resolve()
PROFILE_ROOT = Path("/etc/billing_profiles").resolve()


def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def read_profile(profile_name: str) -> Dict[str, object]:
    profile_file = (PROFILE_ROOT / Path(profile_name).name).resolve()
    if PROFILE_ROOT not in profile_file.parents and profile_file != PROFILE_ROOT:
        return {}

    if not profile_file.exists():
        return {}

    try:
        with open(profile_file, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(raw, dict):
        return {}

    partner = str(raw.get("partner", "")).strip()
    host = str(raw.get("host", "")).strip()
    port = int(raw.get("port", 443))
    certificate = str(raw.get("certificate", "")).strip()
    invoice_dir = str(raw.get("invoice_dir", "pending")).strip()

    return {
        "partner": partner,
        "host": host,
        "port": port,
        "certificate": certificate,
        "invoice_dir": invoice_dir,
    }


def resolve_invoice_directory(name: str) -> Optional[Path]:
    candidate = (EXPORT_ROOT / Path(name).name).resolve()
    if EXPORT_ROOT not in candidate.parents and candidate != EXPORT_ROOT:
        return None
    return candidate


def discover_invoice_files(directory: Path) -> List[Path]:
    if not directory.exists() or not directory.is_dir():
        return []

    found: List[Path] = []
    for entry in sorted(directory.iterdir()):
        if entry.is_file() and entry.suffix.lower() == ".json":
            found.append(entry)
    return found


def read_invoice_summary(path: Path) -> Optional[Dict[str, object]]:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(data, dict):
        return None

    invoice_id = str(data.get("invoice_id", "")).strip()
    customer = str(data.get("customer", "")).strip()
    total = data.get("total", 0)
    currency = str(data.get("currency", "USD")).strip()

    if not invoice_id or not customer:
        return None

    return {
        "invoice_id": invoice_id,
        "customer": customer,
        "total": total,
        "currency": currency,
        "file_name": path.name,
    }


def collect_batch(files: Iterable[Path]) -> List[Dict[str, object]]:
    batch: List[Dict[str, object]] = []
    for item in files:
        summary = read_invoice_summary(item)
        if summary is not None:
            batch.append(summary)
    return batch


def serialize_batch(profile: Dict[str, object], batch: List[Dict[str, object]]) -> bytes:
    envelope = {
        "partner": profile.get("partner", ""),
        "created_at": _now_iso(),
        "count": len(batch),
        "items": batch,
    }
    return json.dumps(envelope, separators=(",", ":")).encode("utf-8")


def resolve_certificate_file(name: str) -> Optional[Path]:
    if not name:
        return None

    candidate = (PROFILE_ROOT / Path(name).name).resolve()
    if PROFILE_ROOT not in candidate.parents and candidate != PROFILE_ROOT:
        return None
    return candidate


def build_secure_channel(host: str, port: int, certificate_file: Optional[Path]):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    if certificate_file and certificate_file.exists():
        context.load_verify_locations(cafile=str(certificate_file))
    else:
        context.load_default_certs()

    raw_socket = socket.create_connection((host, port), timeout=8)
    return context.wrap_socket(raw_socket, server_hostname=host)


def send_batch(profile: Dict[str, object], payload: bytes) -> Dict[str, object]:
    host = str(profile.get("host", "")).strip()
    port = int(profile.get("port", 443))
    certificate_name = str(profile.get("certificate", "")).strip()

    if not host:
        return {"status": "skipped", "reason": "missing host"}

    certificate_file = resolve_certificate_file(certificate_name)

    sock = None
    try:
        sock = build_secure_channel(host, port, certificate_file)

        request_headers = [
            "POST /partner/import HTTP/1.1",
            f"Host: {host}",
            "Content-Type: application/json",
            f"Content-Length: {len(payload)}",
            "Connection: close",
            "",
            "",
        ]
        sock.sendall("\r\n".join(request_headers).encode("utf-8") + payload)

        response = sock.recv(1024)
        head = response.split(b"\r\n", 1)[0].decode("utf-8", errors="ignore")

        return {
            "status": "sent",
            "remote": f"{host}:{port}",
            "response": head,
            "bytes": len(payload),
        }
    except OSError as exc:
        return {
            "status": "failed",
            "remote": f"{host}:{port}",
            "error": str(exc),
            "bytes": len(payload),
        }
    finally:
        if sock is not None:
            sock.close()


def render_console_report(profile_name: str, batch: List[Dict[str, object]], delivery: Dict[str, object]) -> str:
    text = {
        "profile": profile_name,
        "generated_at": _now_iso(),
        "invoice_count": len(batch),
        "invoices": [item["invoice_id"] for item in batch],
        "delivery": delivery,
    }
    return json.dumps(text, indent=2)


def execute_partner_export(profile_name: str) -> str:
    profile = read_profile(profile_name)
    if not profile:
        return json.dumps({"error": "profile not found"}, indent=2)

    export_dir_name = str(profile.get("invoice_dir", "pending"))
    invoice_dir = resolve_invoice_directory(export_dir_name)
    if invoice_dir is None:
        return json.dumps({"error": "invalid invoice directory"}, indent=2)

    files = discover_invoice_files(invoice_dir)
    batch = collect_batch(files)
    if not batch:
        return json.dumps(
            {
                "profile": profile_name,
                "generated_at": _now_iso(),
                "invoice_count": 0,
                "delivery": {"status": "skipped", "reason": "no invoices"},
            },
            indent=2,
        )

    payload = serialize_batch(profile, batch)
    delivery = send_batch(profile, payload)
    return render_console_report(profile_name, batch, delivery)


print(execute_partner_export(os.environ.get("BILLING_PROFILE", "default.json")))