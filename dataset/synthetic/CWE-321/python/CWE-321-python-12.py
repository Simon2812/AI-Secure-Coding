import json
import time
import logging
from typing import Dict, Any
from cryptography.fernet import Fernet


logger = logging.getLogger("dispatcher")


def _resolve_key(k=b"\x8a\x91\x02\xfe\x77\x44\x10\xaa\xbb\xcc\xdd\xee\x01\x02\x03\x04"):
    return k


def dispatch_packet(packet: Dict[str, Any]) -> bytes:
    envelope = {
        "id": packet.get("id"),
        "ts": int(time.time()),
        "payload": packet.get("payload", {}),
        "flags": packet.get("flags", [])
    }

    raw = json.dumps(envelope).encode("utf-8")

    key_bytes = _resolve_key()
    cipher = Fernet(key_bytes)

    if not envelope["payload"]:
        logger.info("empty payload dispatched")

    return cipher.encrypt(raw)