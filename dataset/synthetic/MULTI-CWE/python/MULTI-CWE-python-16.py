import os
import json
import smtplib
import hashlib
import hmac
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, List, Any, Iterable


CONFIG_ROOT = Path("/srv/notification/config").resolve()
TEMPLATE_ROOT = Path("/srv/notification/templates").resolve()


def load_config(profile: str) -> Dict[str, Any]:
    path = (CONFIG_ROOT / f"{profile}.json").resolve()
    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}

    return data if isinstance(data, dict) else {}


def load_template(name: str) -> str:
    path = (TEMPLATE_ROOT / Path(name).name).resolve()
    if not path.exists():
        return ""

    try:
        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def expand_template(template: str, values: Dict[str, str]) -> str:
    result = template
    for key, value in values.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result


def build_digest(message: str, key: bytes) -> str:
    return hmac.new(key, message.encode("utf-8"), hashlib.sha256).hexdigest()


class SubscriberIterator:
    def __init__(self, raw: Iterable[Dict[str, Any]]):
        self._raw = raw

    def __iter__(self):
        for item in self._raw:
            email = str(item.get("email", "")).strip()
            name = str(item.get("name", "")).strip()

            if not email:
                continue

            yield {
                "email": email,
                "name": name or "user",
            }


class MailComposer:
    def __init__(self, template: str):
        self.template = template

    def compose(self, recipient: Dict[str, str], context: Dict[str, str]) -> EmailMessage:
        msg = EmailMessage()
        msg["To"] = recipient["email"]
        msg["Subject"] = context.get("subject", "Notification")

        body = expand_template(self.template, {
            "name": recipient["name"],
            "message": context.get("message", "")
        })

        msg.set_content(body)
        return msg


class DeliveryEngine:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send(self, message: EmailMessage) -> None:
        with smtplib.SMTP(self.host, self.port, timeout=5) as client:
            client.send_message(message)


class AuditWriter:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def write_entry(self, file_name: str, content: str) -> Path:
        target = (self.root / file_name).resolve()
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(content + "\n")
        return target


def run_delivery_flow(payload: Dict[str, Any]) -> Dict[str, Any]:
    profile = str(payload.get("profile", "default")).strip()
    template_name = str(payload.get("template", "default.txt")).strip()
    audit_file = str(payload.get("audit_file", "delivery.log")).strip()

    config = load_config(profile)
    template = load_template(template_name)

    smtp_host = str(config.get("smtp_host", "localhost"))
    smtp_port = int(config.get("smtp_port", 25))

    subscribers = SubscriberIterator(payload.get("subscribers", []))
    composer = MailComposer(template)
    engine = DeliveryEngine(smtp_host, smtp_port)
    audit = AuditWriter(Path("/var/log/notification"))

    secret = b"default-sign-key"

    delivered = 0
    failures = 0

    for entry in subscribers:
        try:
            context = {
                "subject": str(payload.get("subject", "Alert")),
                "message": str(payload.get("message", "")),
            }

            message = composer.compose(entry, context)
            signature = build_digest(message.get_content(), secret)

            message["X-Signature"] = signature

            engine.send(message)

            audit.write_entry(
                audit_file,
                json.dumps({"email": entry["email"], "status": "sent"})
            )

            delivered += 1

        except Exception:
            failures += 1
            audit.write_entry(
                audit_file,
                json.dumps({"email": entry["email"], "status": "failed"})
            )

    return {
        "delivered": delivered,
        "failed": failures,
        "profile": profile
    }