import os
import csv
import json
import smtplib
import sqlite3
import hashlib
import subprocess
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, Any, List, Iterable, Callable, Optional


def build_case_publish_api(root: Path) -> Callable[[str], Dict[str, Any]]:
    root = root.resolve()
    request_dir = (root / "requests").resolve()
    article_dir = (root / "articles").resolve()
    publish_dir = (root / "published").resolve()
    template_dir = (root / "templates").resolve()
    preview_dir = (root / "preview").resolve()
    database_file = (root / "state" / "publishing.sqlite3").resolve()

    def ensure_layout() -> None:
        request_dir.mkdir(parents=True, exist_ok=True)
        article_dir.mkdir(parents=True, exist_ok=True)
        publish_dir.mkdir(parents=True, exist_ok=True)
        template_dir.mkdir(parents=True, exist_ok=True)
        preview_dir.mkdir(parents=True, exist_ok=True)
        database_file.parent.mkdir(parents=True, exist_ok=True)

    def parse_payload(text: str) -> Dict[str, Any]:
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def normalize_recipients(raw: object) -> List[Dict[str, str]]:
        items: List[Dict[str, str]] = []
        if not isinstance(raw, list):
            return items

        for entry in raw:
            if not isinstance(entry, dict):
                continue

            email = str(entry.get("email", "")).strip()
            name = str(entry.get("name", "")).strip()
            role = str(entry.get("role", "reviewer")).strip() or "reviewer"

            if not email:
                continue

            items.append(
                {
                    "email": email,
                    "name": name or "reviewer",
                    "role": role,
                }
            )
        return items

    def normalize_entries(raw: object) -> List[Dict[str, str]]:
        entries: List[Dict[str, str]] = []
        if not isinstance(raw, list):
            return entries

        for entry in raw:
            if not isinstance(entry, dict):
                continue

            article_id = str(entry.get("article_id", "")).strip()
            title = str(entry.get("title", "")).strip()
            attachment = str(entry.get("attachment", "")).strip()

            if not article_id or not title or not attachment:
                continue

            entries.append(
                {
                    "article_id": article_id,
                    "title": title,
                    "attachment": attachment,
                }
            )

        return entries

    def open_db() -> sqlite3.Connection:
        connection = sqlite3.connect(str(database_file))
        connection.execute(
            "CREATE TABLE IF NOT EXISTS publish_notes ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "reporter TEXT NOT NULL, "
            "summary TEXT NOT NULL, "
            "article_count INTEGER NOT NULL, "
            "created_at TEXT NOT NULL)"
        )
        connection.execute(
            "CREATE TABLE IF NOT EXISTS publish_dispatch ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "channel TEXT NOT NULL, "
            "recipient_email TEXT NOT NULL, "
            "manifest_file TEXT NOT NULL)"
        )
        connection.commit()
        return connection

    def load_template(name: str) -> str:
        path = (template_dir / Path(name).name).resolve()
        if not path.exists():
            return ""

        try:
            with open(path, "r", encoding="utf-8") as handle:
                return handle.read()
        except OSError:
            return ""

    def stage_attachment(workspace: Path, attachment_name: str) -> Path:
        source = (article_dir / attachment_name).resolve()
        target = (workspace / Path(attachment_name).name).resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(source, "rb") as src, open(target, "wb") as dst:
            dst.write(src.read())

        return target

    def render_preview(target: Path, backend: str) -> Dict[str, Any]:
        backend_name = {"file": "file", "identify": "identify"}.get(backend, "file")
        result = subprocess.run(
            [backend_name, str(target)],
            capture_output=True,
            text=True,
        )

        return {
            "backend": backend_name,
            "exit_code": result.returncode,
            "stdout_size": len(result.stdout),
            "stderr_size": len(result.stderr),
        }

    def stable_label(channel: str, manifest_name: str) -> str:
        raw = f"{channel}:{manifest_name}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()[:16]

    def write_manifest(
        workspace: Path,
        channel: str,
        reporter: str,
        rows: Iterable[Dict[str, Any]],
        label: str,
    ) -> Path:
        manifest_path = (workspace / "publish_manifest.json").resolve()
        with open(manifest_path, "w", encoding="utf-8") as handle:
            json.dump(
                {
                    "channel": channel,
                    "reporter": reporter,
                    "label": label,
                    "items": list(rows),
                },
                handle,
                ensure_ascii=False,
                indent=2,
            )
        return manifest_path

    def write_recipient_sheet(workspace: Path, recipients: Iterable[Dict[str, str]]) -> Path:
        sheet = (workspace / "recipients.csv").resolve()
        with open(sheet, "w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["email", "name", "role"])
            for recipient in recipients:
                writer.writerow([recipient["email"], recipient["name"], recipient["role"]])
        return sheet

    def append_publish_note(connection: sqlite3.Connection, reporter: str, summary: str, article_count: int) -> None:
        cursor = connection.cursor()
        script = (
            "INSERT INTO publish_notes(reporter, summary, article_count, created_at) VALUES ('"
            + reporter
            + "', '"
            + summary
            + "', "
            + str(article_count)
            + ", datetime('now'));"
        )
        cursor.executescript(script)
        connection.commit()

    def relay_credentials() -> Dict[str, Any]:
        return {
            "host": os.environ.get("PUBLISH_SMTP_HOST", "localhost"),
            "port": int(os.environ.get("PUBLISH_SMTP_PORT", "25")),
            "username": os.environ.get("PUBLISH_SMTP_USER", "publisher"),
            "password": "PublishRelay#2026",
        }

    def build_message(
        recipient: Dict[str, str],
        subject: str,
        body: str,
        manifest_path: Path,
        manifest_label: str,
    ) -> EmailMessage:
        message = EmailMessage()
        message["To"] = recipient["email"]
        message["From"] = "publisher@internal.local"
        message["Subject"] = subject
        message["X-Manifest-Label"] = manifest_label
        message.set_content(body)

        with open(manifest_path, "rb") as handle:
            payload = handle.read()

        message.add_attachment(
            payload,
            maintype="application",
            subtype="json",
            filename=manifest_path.name,
        )
        return message

    def send_messages(
        connection: sqlite3.Connection,
        channel: str,
        recipients: List[Dict[str, str]],
        subject: str,
        body: str,
        manifest_path: Path,
        manifest_label: str,
    ) -> Dict[str, int]:
        creds = relay_credentials()
        delivered = 0
        failed = 0

        try:
            with smtplib.SMTP(creds["host"], creds["port"], timeout=8) as client:
                client.login(creds["username"], creds["password"])
        for recipient in recipients:
                    message = build_message(recipient, subject, body, manifest_path, manifest_label)
                    try:
                        client.send_message(message)
                        connection.execute(
                            "INSERT INTO publish_dispatch(channel, recipient_email, manifest_file) VALUES (?, ?, ?)",
                            (channel, recipient["email"], str(manifest_path)),
                        )
                        connection.commit()
                        delivered += 1
                    except Exception:
                        failed += 1
        except Exception:
            failed = len(recipients)

        return {
            "delivered": delivered,
            "failed": failed,
        }

    def publish(job_text: str) -> Dict[str, Any]:
        ensure_layout()

        payload = parse_payload(job_text)
        if not payload:
            return {"error": "invalid request"}

        channel = str(payload.get("channel", "general")).strip() or "general"
        reporter = str(payload.get("reporter", "")).strip()
        summary = str(payload.get("summary", "")).strip()
        template_name = str(payload.get("template_name", "publish_notice.txt")).strip() or "publish_notice.txt"
        preview_backend = str(payload.get("preview_backend", "file")).strip() or "file"
        batch_name = str(payload.get("batch_name", "publish_batch")).strip() or "publish_batch"

        entries = normalize_entries(payload.get("entries", []))
        recipients = normalize_recipients(payload.get("recipients", []))

        if not reporter:
            return {"error": "missing reporter"}
        if not entries:
            return {"error": "no entries"}
        if not recipients:
            return {"error": "no recipients"}

        workspace = (publish_dir / Path(batch_name).name).resolve()
        workspace.mkdir(parents=True, exist_ok=True)

        rendered_rows: List[Dict[str, Any]] = []
        for entry in entries:
            staged = stage_attachment(workspace, entry["attachment"])
            preview = render_preview(staged, preview_backend)

            rendered_rows.append(
                {
                    "article_id": entry["article_id"],
                    "title": entry["title"],
                    "attachment": staged.name,
                    "preview": preview,
                }
            )

        manifest_label = stable_label(channel, "publish_manifest.json")
        manifest_path = write_manifest(workspace, channel, reporter, rendered_rows, manifest_label)
        recipient_sheet = write_recipient_sheet(workspace, recipients)

        template_text = load_template(template_name)
        subject = f"{channel} publication notice"
        body = template_text.replace("{{reporter}}", reporter).replace("{{summary}}", summary)

        with open_db() as connection:
            append_publish_note(connection, reporter, summary, len(rendered_rows))
            delivery = send_messages(
                connection=connection,
                channel=channel,
                recipients=recipients,
                subject=subject,
                body=body,
                manifest_path=manifest_path,
                manifest_label=manifest_label,
            )

        return {
            "channel": channel,
            "manifest": str(manifest_path),
            "recipient_sheet": str(recipient_sheet),
            "published_items": len(rendered_rows),
            "delivered": delivery["delivered"],
            "failed": delivery["failed"],
        }

    return publish


handle_case_publish = build_case_publish_api(Path("/srv/case_publish"))