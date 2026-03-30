import os
import json
import hmac
import hashlib
import sqlite3
from typing import Dict, Any


DB_PATH = "/srv/integrations/webhooks.db"


class WebhookStore:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_webhook(self, name: str) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_path)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT endpoint, active FROM webhooks WHERE name = ?",
                (name,),
            )
            row = cur.fetchone()
            if not row:
                return {}
            return {
                "endpoint": row[0],
                "active": bool(row[1]),
            }
        finally:
            conn.close()


class SignatureService:
    def __init__(self):
        self.secret = b"internal-signing-key"

    def build_payload(self, event: Dict[str, Any]) -> bytes:
        body = {
            "type": event.get("type"),
            "data": event.get("data", {}),
        }
        return json.dumps(body, separators=(",", ":")).encode("utf-8")

    def sign(self, payload: bytes) -> bytes:
        signature = hmac.new(self.secret, payload, hashlib.sha256).digest()
        return payload + b"." + signature

    def verify(self, raw: bytes) -> bool:
        try:
            payload, sig = raw.rsplit(b".", 1)
        except ValueError:
            return False

        expected = hmac.new(self.secret, payload, hashlib.sha256).digest()
        return hmac.compare_digest(sig, expected)


class DeliveryService:
    def __init__(self, store: WebhookStore):
        self.store = store

    def deliver(self, name: str, event: Dict[str, Any]) -> Dict[str, Any]:
        webhook = self.store.get_webhook(name)
        if not webhook or not webhook.get("active"):
            return {"status": "skipped"}

        signer = SignatureService()
        payload = signer.build_payload(event)
        signed = signer.sign(payload)

        return {
            "endpoint": webhook["endpoint"],
            "payload_size": len(signed),
        }


def load_event() -> Dict[str, Any]:
    raw = os.environ.get("EVENT_JSON", "{}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def main():
    webhook_name = os.environ.get("WEBHOOK", "default")
    event = load_event()

    store = WebhookStore(DB_PATH)
    service = DeliveryService(store)

    result = service.deliver(webhook_name, event)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()