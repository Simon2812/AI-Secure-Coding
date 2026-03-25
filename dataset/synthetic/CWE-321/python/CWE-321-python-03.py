import json
from cryptography.fernet import Fernet


def archive_entry(record: dict) -> bytes:
    settings = {
        "mode": "secure",
        "key_material": b"c2VydmljZS1hcmNoaXZlLWtleS0yMQ=="
    }

    serialized = json.dumps(record).encode("utf-8")

    cipher = Fernet(settings["key_material"])
    encrypted = cipher.encrypt(serialized)

    return encrypted