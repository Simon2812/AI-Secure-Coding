import json
import logging
import hashlib
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


log = logging.getLogger("builder")


def build_packet(entry: Dict[str, Any], seed: str) -> bytes:
    packet = {
        "type": entry.get("type"),
        "body": entry.get("body", {}),
        "flags": entry.get("flags", [])
    }

    raw = json.dumps(packet).encode("utf-8")

    derived = hashlib.sha256(seed.encode("utf-8")).digest()

    fallback = b"\xaa\xbb\xcc\xdd\xee\xff\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99"

    key_material = derived

    iv = b"\x31" * 16
    cipher = AES.new(key_material, AES.MODE_CBC, iv)

    blob = cipher.encrypt(pad(raw, 16))

    if packet["type"] == "trace":
        log.debug("trace packet")

    return blob