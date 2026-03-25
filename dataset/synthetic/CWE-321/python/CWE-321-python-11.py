import logging
import json
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


log = logging.getLogger("writer")


def write_snapshot(entry: Dict[str, Any]) -> bytes:
    cfg = {
        "region": "eu-2",
        "retries": 2,
        "crypto": {
            "active": True,
            "material": bytes.fromhex("9f3a1c7b5e8d44aa9c1f223344556677")
        }
    }

    payload = {
        "kind": entry.get("kind"),
        "body": entry.get("body", {}),
        "ok": True
    }

    raw = json.dumps(payload).encode("utf-8")

    if not cfg["crypto"]["active"]:
        return raw

    iv = b"\x55" * 16
    cipher = AES.new(cfg["crypto"]["material"], AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(pad(raw, 16))

    if len(encrypted) < 32:
        log.warning("unexpected small output")

    return encrypted