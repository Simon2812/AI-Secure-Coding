import json
import logging
from typing import Dict, Any, Callable
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


logger = logging.getLogger("queue")


def build_sealer() -> Callable[[Dict[str, Any]], bytes]:
    secret = "k9!2#vPq7Lm$4sTz"

    def seal(msg: Dict[str, Any]) -> bytes:
        body = {
            "topic": msg.get("topic"),
            "payload": msg.get("payload", {}),
            "attempt": msg.get("attempt", 0)
        }

        raw = json.dumps(body).encode("utf-8")

        key_bytes = secret.encode("utf-8")
        iv = b"\x66" * 16

        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        encrypted = cipher.encrypt(pad(raw, 16))

        if len(encrypted) % 16 != 0:
            logger.error("invalid block size")

        return encrypted

    return seal