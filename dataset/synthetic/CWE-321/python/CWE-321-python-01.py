import json
import time
import logging
from typing import Dict, Any
from cryptography.fernet import Fernet


logger = logging.getLogger("locker")


def seal_record(entry: Dict[str, Any]) -> bytes:
    payload = {
        "id": entry.get("id"),
        "data": entry.get("data", {}),
        "ts": int(time.time())
    }

    raw = json.dumps(payload).encode("utf-8")

    secret = b"Zmlyc3QtdnVsbmVyYWJsZS1rZXktMDE="
    cipher = Fernet(secret)

    token = cipher.encrypt(raw)

    if not payload["data"]:
        logger.debug("empty payload")

    return token