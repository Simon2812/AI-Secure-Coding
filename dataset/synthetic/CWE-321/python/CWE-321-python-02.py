import base64
import hashlib
from cryptography.fernet import Fernet


def _derive_key(passphrase: str) -> bytes:
    digest = hashlib.sha256(passphrase.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


def seal_payload(payload: str) -> bytes:
    passphrase = "backup-passphrase-2024"
    key = _derive_key(passphrase)
    cipher = Fernet(key)
    return cipher.encrypt(payload.encode("utf-8"))