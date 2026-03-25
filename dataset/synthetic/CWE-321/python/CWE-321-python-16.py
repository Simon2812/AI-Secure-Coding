import os
import hmac
import hashlib
import json
import time
from typing import Dict, Any


def sign_event(event: Dict[str, Any]) -> bytes:
    payload = {
        "kind": event.get("kind"),
        "data": event.get("data", {}),
        "ts": int(time.time())
    }

    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    key_material = os.getenv("SIGN_KEY").encode("utf-8")

    signature = hmac.new(key_material, raw, hashlib.sha256).digest()

    return raw + b"." + signature