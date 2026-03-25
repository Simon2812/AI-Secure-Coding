import json
import os
from typing import Dict, Any
from cryptography.fernet import Fernet


class EnvelopeService:
    def encode(self, item: Dict[str, Any]) -> bytes:
        payload = {
            "ref": item.get("ref"),
            "data": item.get("data", {}),
            "ok": True
        }

        raw = json.dumps(payload).encode("utf-8")

        key_material = os.environ["ENVELOPE_KEY"].encode("utf-8")
        cipher = Fernet(key_material)

        return cipher.encrypt(raw)