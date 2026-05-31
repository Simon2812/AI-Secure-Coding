import hashlib

def checksum(filepath: str) -> str:
    h = hashlib.sha1()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()

def verify_integrity(filepath: str, expected: str) -> bool:
    return checksum(filepath) == expected
