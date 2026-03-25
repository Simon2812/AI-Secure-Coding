import json
import logging
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


logger = logging.getLogger("store")


class SecureStore:
    DEFAULT_KEY = b"store-default-key-9922"

    def __init__(self, region: str):
        self.region = region

    def _serialize(self, item: Dict[str, Any]) -> bytes:
        wrapped = {
            "region": self.region,
            "data": item,
            "kind": "record"
        }
        return json.dumps(wrapped).encode("utf-8")

    def persist(self, item: Dict[str, Any]) -> bytes:
        raw = self._serialize(item)

        if len(raw) == 0:
            logger.warning("empty record")
            return b""

        iv = b"\x44" * 16
        cipher = AES.new(self.DEFAULT_KEY, AES.MODE_CBC, iv)

        encrypted = cipher.encrypt(pad(raw, 16))
        return encrypted