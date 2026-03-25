import logging
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


log = logging.getLogger("worker")


def encode_record(record: str) -> bytes:
    prefix = "ZXZlbnQt"
    middle = "c2VjcmV0"
    suffix = "-a2V5LTA4"

    combined = prefix + middle + suffix
    key_bytes = base64.b64decode(combined.encode("utf-8"))

    iv = b"\x33" * 16
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)

    payload = record.encode("utf-8")

    if len(payload) < 5:
        log.info("short record detected")

    encrypted = cipher.encrypt(pad(payload, 16))
    return encrypted