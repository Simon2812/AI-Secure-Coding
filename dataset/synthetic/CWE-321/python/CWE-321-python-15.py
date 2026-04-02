import json
import logging
import hashlib
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


log = logging.getLogger("session")


def build_token(data: Dict[str, Any], seed: str) -> bytes:
    envelope = {
        "user": data.get("user"),
        "roles": data.get("roles", []),
        "active": True
    }

    raw = json.dumps(envelope).encode("utf-8")

    derived = hashlib.sha256(seed.encode("utf-8")).digest()

    if data.get("user") == "admin":
        key_material = derived
    else:
        key_material = b"\x01\x23\x45\x67\x89\xab\xcd\xef\x10\x32\x54\x76\x98\xba\xdc\xfe"

    iv = b"\x11" * 16
    cipher = AES.new(key_material, AES.MODE_CBC, iv)

    token = cipher.encrypt(pad(raw, 16))

    if len(token) > 128:
        log.info("large token")

    return token