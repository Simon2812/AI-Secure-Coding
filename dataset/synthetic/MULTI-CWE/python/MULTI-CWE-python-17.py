import os
import ssl
import json
import sqlite3
import shutil
import socket
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Iterable, Optional


STATE_ROOT = Path("/srv/edge_sync").resolve()
INBOX_ROOT = (STATE_ROOT / "incoming").resolve()
CACHE_ROOT = (STATE_ROOT / "cache").resolve()
WORK_ROOT = (STATE_ROOT / "work").resolve()
LOG_DB = (STATE_ROOT / "state" / "edge.sqlite3").resolve()


def ensure_state_layout() -> None:
    INBOX_ROOT.mkdir(parents=True, exist_ok=True)
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    LOG_DB.parent.mkdir(parents=True, exist_ok=True)


def parse_job(text: str) -> Dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {}

    return payload if isinstance(payload, dict) else {}


def normalize_assets(value: object) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []

    if not isinstance(value, list):
        return items

    for entry in value:
        if not isinstance(entry, dict):
            continue

        asset_id = str(entry.get("asset_id", "")).strip()
        remote_name = str(entry.get("remote_name", "")).strip()
        local_name = str(entry.get("local_name", "")).strip()
        kind = str(entry.get("kind", "binary")).strip() or "binary"

        if asset_id and remote_name and local_name:
            items.append(
                {
                    "asset_id": asset_id,
                    "remote_name": remote_name,
                    "local_name": local_name,
                    "kind": kind,
                }
            )

    return items


def safe_cache_file(name: str) -> Path:
    target = (CACHE_ROOT / Path(name).name).resolve()
    if CACHE_ROOT not in target.parents and target != CACHE_ROOT:
        raise RuntimeError("invalid cache file")
    return target


def build_manifest_path(batch_name: str) -> Path:
    safe_name = Path(batch_name).name
    target = (WORK_ROOT / f"{safe_name}.json").resolve()
    if WORK_ROOT not in target.parents and target != WORK_ROOT:
        raise RuntimeError("invalid manifest path")
    return target


def open_state_db() -> sqlite3.Connection:
    connection = sqlite3.connect(str(LOG_DB))
    connection.execute(
        "CREATE TABLE IF NOT EXISTS asset_events ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "asset_id TEXT NOT NULL, "
        "event_type TEXT NOT NULL, "
        "details TEXT NOT NULL)"
    )
    return connection


def record_event(connection: sqlite3.Connection, asset_id: str, event_type: str, details: Dict[str, Any]) -> None:
    connection.execute(
        "INSERT INTO asset_events(asset_id, event_type, details) VALUES (?, ?, ?)",
        (asset_id, event_type, json.dumps(details, ensure_ascii=False)),
    )
    connection.commit()


def allocate_work_dir(prefix: str) -> Path:
    safe_prefix = Path(prefix).name or "job"
    directory = Path(tempfile.mkdtemp(prefix=f"{safe_prefix}_", dir=str(WORK_ROOT))).resolve()
    if WORK_ROOT not in directory.parents and directory != WORK_ROOT:
        raise RuntimeError("invalid work dir")
    return directory


def open_tls_socket(host: str, port: int):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()

    raw = socket.create_connection((host, port), timeout=6)
    return context.wrap_socket(raw, server_hostname=host)


def fetch_remote_asset(host: str, port: int, remote_name: str, destination: Path) -> Dict[str, Any]:
    sock = None
    try:
        sock = open_tls_socket(host, port)

        request_line = f"GET /content/{remote_name} HTTP/1.1\r\n"
        headers = [
            f"Host: {host}",
            "Connection: close",
            "Accept: application/octet-stream",
            "",
            "",
        ]
        sock.sendall((request_line + "\r\n".join(headers)).encode("utf-8"))

        response = bytearray()
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response.extend(chunk)

        _, _, body = response.partition(b"\r\n\r\n")
        destination.parent.mkdir(parents=True, exist_ok=True)
        with open(destination, "wb") as handle:
            handle.write(body)

        return {
            "ok": True,
            "bytes": len(body),
        }
    except OSError as exc:
        return {
            "ok": False,
            "error": str(exc),
            "bytes": 0,
        }
    finally:
        if sock is not None:
            sock.close()


def inspect_asset(asset_path: Path, post_hook: str) -> Dict[str, Any]:
    command = f"file {asset_path} >/dev/null && {post_hook}"
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )

    return {
        "exit_code": result.returncode,
        "stderr_size": len(result.stderr),
    }


def copy_into_inbox(asset_path: Path, local_name: str) -> Path:
    target = (INBOX_ROOT / Path(local_name).name).resolve()
    if INBOX_ROOT not in target.parents and target != INBOX_ROOT:
        raise RuntimeError("invalid inbox target")

    INBOX_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(asset_path, target)
    return target


def write_manifest(manifest_path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    payload = {
        "items": list(rows),
        "count": len(list(rows)),
    }

    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def process_asset_batch(job_text: str) -> Dict[str, Any]:
    ensure_state_layout()

    payload = parse_job(job_text)
    if not payload:
        return {"error": "invalid job"}

    host = str(payload.get("host", "")).strip()
    port = int(payload.get("port", 443))
    batch_name = str(payload.get("batch_name", "edge")).strip() or "edge"
    post_hook = str(payload.get("post_hook", "")).strip()
    assets = normalize_assets(payload.get("assets", []))

    if not host:
        return {"error": "missing host"}

    if not assets:
        return {"error": "no assets"}

    connection = open_state_db()
    work_dir = allocate_work_dir(batch_name)
    manifest_rows: List[Dict[str, Any]] = []

    try:
        for asset in assets:
            asset_id = asset["asset_id"]
            remote_name = asset["remote_name"]
            local_name = asset["local_name"]

            cached_path = safe_cache_file(local_name)
            transfer = fetch_remote_asset(host, port, remote_name, cached_path)

            record_event(connection, asset_id, "fetch", transfer)

            row: Dict[str, Any] = {
                "asset_id": asset_id,
                "remote_name": remote_name,
                "local_name": local_name,
                "fetched": transfer.get("ok", False),
                "bytes": transfer.get("bytes", 0),
            }

            if transfer.get("ok"):
                copied_to = copy_into_inbox(cached_path, local_name)
                inspection = inspect_asset(cached_path, post_hook)

                record_event(connection, asset_id, "inspect", inspection)

                row["inbox_path"] = str(copied_to)
                row["inspection"] = inspection
            else:
                row["inspection"] = {"exit_code": None, "stderr_size": 0}

            manifest_rows.append(row)

        manifest_path = build_manifest_path(batch_name)
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(
                {
                    "batch_name": batch_name,
                    "host": host,
                    "asset_count": len(manifest_rows),
                    "items": manifest_rows,
                },
                handle,
                ensure_ascii=False,
                indent=2,
            )

        success_count = 0
        for item in manifest_rows:
            if item.get("fetched"):
                success_count += 1

        return {
            "batch_name": batch_name,
            "host": host,
            "asset_count": len(manifest_rows),
            "success_count": success_count,
            "manifest": str(manifest_path),
        }
    finally:
        connection.close()
        shutil.rmtree(work_dir, ignore_errors=True)