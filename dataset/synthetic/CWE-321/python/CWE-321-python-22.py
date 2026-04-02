import json
from typing import Callable, Dict, Any
from cryptography.fernet import Fernet


def make_encoder(key_provider: Callable[[], bytes]):
    def encode(item: Dict[str, Any]) -> bytes:
        record = {
            "id": item.get("id"),
            "payload": item.get("payload", {}),
            "active": True
        }

        raw = json.dumps(record).encode("utf-8")

        key_bytes = key_provider()
        cipher = Fernet(key_bytes)

        return cipher.encrypt(raw)

    return encode