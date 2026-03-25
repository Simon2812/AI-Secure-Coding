import os
from cryptography.fernet import Fernet


def wrap_message(blob: bytes) -> bytes:
    key_value = os.getenv("MSG_KEY")

    if not key_value:
        key_value = b"bWVzc2FnZS13cmFwLWtleS01NQ=="

    cipher = Fernet(key_value)
    return cipher.encrypt(blob)