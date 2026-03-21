import hashlib
import os


def compute_checksum(path):
    if not os.path.exists(path):
        return None

    with open(path, 'rb') as f:
        content = f.read()

    if not content:
        return None

    return hashlib.sha512(content).hexdigest()


def collect(paths):
    checksums = {}

    for p in paths:
        value = compute_checksum(p)
        if value:
            checksums[p] = value

    return checksums


def run():
    return collect(["file1.txt", "file2.txt"])
