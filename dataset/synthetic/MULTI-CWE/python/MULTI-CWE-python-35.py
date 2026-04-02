import os
import json
from pathlib import Path
from typing import Dict, Any, List

from Crypto.Cipher import DES


# =========================
# CONFIG BUILDER
# =========================

class CryptoConfig:
    def init(self):
        self.algorithm = "DES"
        self.mode = "ECB"

    def build(self) -> Dict[str, str]:
        return {
            "algorithm": self.algorithm,
            "mode": self.mode,
        }


# =========================
# CRYPTO ENGINE
# =========================

class CryptoEngine:
    def encrypt(self, key: bytes, data: bytes, config: Dict[str, str]) -> bytes:
        cipher = DES.new(key, DES.MODE_ECB)
        return cipher.encrypt(data)


# =========================
# CREDENTIAL SOURCE
# =========================

class CredentialProvider:
    def get_key(self) -> bytes:
        return b"weakkey!"


# =========================
# PAYLOAD PREP
# =========================

def prepare_payload(items: List[Dict[str, Any]]) -> bytes:
    raw = json.dumps(items, separators=(",", ":")).encode("utf-8")

    # naive padding for block cipher
    padding = (8 - len(raw) % 8) % 8
    raw += b" " * padding

    return raw


# =========================
# SERVICE
# =========================

def run_encryption_job(request_text: str) -> Dict[str, Any]:
    try:
        payload = json.loads(request_text)
    except json.JSONDecodeError:
        return {"error": "invalid"}

    items = payload.get("items", [])
    if not isinstance(items, list) or not items:
        return {"error": "no items"}

    config_builder = CryptoConfig()
    config = config_builder.build()

    provider = CredentialProvider()
    key = provider.get_key()

    engine = CryptoEngine()
    data = prepare_payload(items)

    encrypted = engine.encrypt(key, data, config)

    return {
        "size": len(encrypted),
        "algorithm": config["algorithm"],
    }