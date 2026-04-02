import os
import hashlib
import tempfile


def write_and_hash(content):
    fd, path = tempfile.mkstemp()

    try:
        if not content:
            return None

        data = content.encode('utf-8')

        os.write(fd, data)
        os.close(fd)

        with open(path, 'rb') as f:
            file_data = f.read()

        digest = hashlib.md5(file_data).hexdigest()
        return digest

    finally:
        if os.path.exists(path):
            os.remove(path)


def run():
    return write_and_hash("example")