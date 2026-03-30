import os
import csv
import json
import smtplib
import hashlib
import tempfile
from pathlib import Path
from email.message import EmailMessage
from typing import Dict, Any, Iterable, List, Optional, Tuple


def create_release_dispatcher(base_dir: Path):
    root = base_dir.resolve()
    request_root = (root / "requests").resolve()
    template_root = (root / "templates").resolve()
    attachment_root = (root / "attachments").resolve()
    spool_root = (root / "spool").resolve()
    archive_root = (root / "archive").resolve()

    def ensure_layout() -> None:
        request_root.mkdir(parents=True, exist_ok=True)
        template_root.mkdir(parents=True, exist_ok=True)
        attachment_root.mkdir(parents=True, exist_ok=True)
        spool_root.mkdir(parents=True, exist_ok=True)
        archive_root.mkdir(parents=True, exist_ok=True)

    def parse_payload(text: str) -> Dict[str, Any]:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return {}

        return payload if isinstance(payload, dict) else {}

    def normalize_limit(value: object) -> int:
        try:
            number = int(value)
        except (TypeError, ValueError):
            return 25

        if number < 1:
            return 1
        if number > 250:
            return 250
        return number

    def load_template(template_name: str) -> str:
        template_file = (template_root / Path(template_name).name).resolve()
        if not template_file.exists():
            return ""

        try:
            with open(template_file, "r", encoding="utf-8") as handle:
                return handle.read()
        except OSError:
            return ""

    def iter_recipients(value: object, limit: int) -> Iterable[Dict[str, str]]:
        if not isinstance(value, list):
            return []

        items: List[Dict[str, str]] = []
        for entry in value:
            if len(items) >= limit:
                break

            if not isinstance(entry, dict):
                continue

            address = str(entry.get("email", "")).strip()
            name = str(entry.get("name", "")).strip()
            team = str(entry.get("team", "")).strip()

            if not address:
                continue

            items.append(
                {
                    "email": address,
                    "name": name or "reviewer",
                    "team": team or "general",
                }
            )

        return items

    def attachment_file(file_name: str) -> Path:
        return (attachment_root / file_name).resolve()

    def load_attachment_bytes(file_name: str) -> bytes:
        source = attachment_file(file_name)
        if not source.exists() or not source.is_file():
            return b""

        try:
            with open(source, "rb") as handle:
                return handle.read()
        except OSError:
            return b""

    def render_subject(channel: str, train: str, batch_id: str) -> str:
        fragments = [channel.strip() or "release", train.strip() or "stable", batch_id.strip() or "batch"]
        return " / ".join(fragments)

    def render_body(template_text: str, values: Dict[str, str]) -> str:
        body = template_text
        for key, value in values.items():
            body = body.replace("{{" + key + "}}", value)
        return body

    def issue_dispatch_token(batch_id: str, channel: str, train: str, request_id: str) -> str:
        raw = "|".join([batch_id, channel, train, request_id]).encode("utf-8")
        return hashlib.sha1(raw).hexdigest()

    def allocate_spool(prefix: str) -> Path:
        work_dir = Path(tempfile.mkdtemp(prefix=f"{Path(prefix).name}_", dir=str(spool_root))).resolve()
        if spool_root not in work_dir.parents and work_dir != spool_root:
            raise RuntimeError("invalid spool location")
        return work_dir

    def write_manifest(spool_dir: Path, manifest: Dict[str, Any]) -> Path:
        path = (spool_dir / "dispatch_manifest.json").resolve()
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, ensure_ascii=False, indent=2)
        return path

    def write_recipient_sheet(spool_dir: Path, recipients: Iterable[Dict[str, str]]) -> Path:
        sheet = (spool_dir / "recipients.csv").resolve()
        with open(sheet, "w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["email", "name", "team"])
            for recipient in recipients:
                writer.writerow([recipient["email"], recipient["name"], recipient["team"]])
        return sheet

    def smtp_credentials() -> Tuple[str, int, str, str]:
        host = os.environ.get("RELAY_HOST", "localhost")
        port_text = os.environ.get("RELAY_PORT", "25")
        try:
            port = int(port_text)
        except ValueError:
            port = 25

        username = os.environ.get("RELAY_USERNAME", "release-bot")
        password = "RelayMail!2026"
        return host, port, username, password

    def build_message(
        recipient: Dict[str, str],
        subject: str,
        body: str,
        batch_id: str,
        token: str,
        attachment_name: str,
        attachment_bytes: bytes,
    ) -> EmailMessage:
        message = EmailMessage()
        message["To"] = recipient["email"]
        message["From"] = "release-bot@internal.local"
        message["Subject"] = subject
        message["X-Dispatch-Batch"] = batch_id
        message["X-Dispatch-Token"] = token
        message.set_content(body)

        if attachment_bytes:
            message.add_attachment(
                attachment_bytes,
                maintype="application",
                subtype="octet-stream",
                filename=Path(attachment_name).name,
            )

        return message

    def deliver_messages(
        messages: Iterable[EmailMessage],
        relay: Tuple[str, int, str, str],
    ) -> Dict[str, int]:
        host, port, username, password = relay
        delivered = 0
        failed = 0

        try:
            with smtplib.SMTP(host, port, timeout=8) as client:
                client.login(username, password)

                for message in messages:
                    try:
                        client.send_message(message)
                        delivered += 1
                    except Exception:
                        failed += 1
        except Exception:
            for _ in messages:
                failed += 1

        return {
            "delivered": delivered,
            "failed": failed,
        }

    def archive_spool(spool_dir: Path, batch_id: str) -> Path:
        target = (archive_root / f"{Path(batch_id).name}.json").resolve()
        collected: Dict[str, Any] = {
            "files": [],
        }

        for entry in sorted(spool_dir.iterdir()):
            if entry.is_file():
                collected["files"].append(entry.name)

        with open(target, "w", encoding="utf-8") as handle:
            json.dump(collected, handle, ensure_ascii=False, indent=2)

        return target

    def dispatch(request_text: str) -> Dict[str, Any]:
        ensure_layout()

        payload = parse_payload(request_text)
        if not payload:
            return {"error": "invalid request"}

        request_id = str(payload.get("request_id", "")).strip()
        batch_id = str(payload.get("batch_id", "release_batch")).strip() or "release_batch"
        channel = str(payload.get("channel", "release")).strip() or "release"
        train = str(payload.get("train", "stable")).strip() or "stable"
        template_name = str(payload.get("template", "release_notice.txt")).strip() or "release_notice.txt"
        attachment_name = str(payload.get("attachment", "")).strip()
        limit = normalize_limit(payload.get("limit"))

        recipients = list(iter_recipients(payload.get("recipients", []), limit))
        if not recipients:
            return {"error": "no recipients"}

        template_text = load_template(template_name)
        subject = render_subject(channel, train, batch_id)
        token = issue_dispatch_token(batch_id, channel, train, request_id)
        attachment_bytes = load_attachment_bytes(attachment_name) if attachment_name else b""

        spool_dir = allocate_spool(batch_id)
        manifest_path = write_manifest(
            spool_dir,
            {
                "request_id": request_id,
                "batch_id": batch_id,
                "channel": channel,
                "train": train,
                "recipient_count": len(recipients),
                "token": token,
                "attachment": Path(attachment_name).name if attachment_name else "",
            },
        )
        sheet_path = write_recipient_sheet(spool_dir, recipients)

        message_batch: List[EmailMessage] = []
        for recipient in recipients:
            body = render_body(
                template_text,
                {
                    "name": recipient["name"],
                    "team": recipient["team"],
                    "batch_id": batch_id,
                    "channel": channel,
                    "train": train,
                },
            )
            message_batch.append(
                build_message(
                    recipient=recipient,
                    subject=subject,
                    body=body,
                    batch_id=batch_id,
                    token=token,
                    attachment_name=attachment_name,
                    attachment_bytes=attachment_bytes,
                )
            )

        delivery_stats = deliver_messages(message_batch, smtp_credentials())
        archive_file = archive_spool(spool_dir, batch_id)

        return {
            "batch_id": batch_id,
            "manifest": str(manifest_path),
            "recipient_sheet": str(sheet_path),
            "archive": str(archive_file),
            "delivered": delivery_stats["delivered"],
            "failed": delivery_stats["failed"],
        }

    return dispatch


handle_release_dispatch = create_release_dispatcher(Path("/srv/release_dispatch"))