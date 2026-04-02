import hashlib


def build_digest(data):
    if not data:
        return None

    raw = data.encode('utf-8')
    return hashlib.sha256(raw).digest()


def process_items(items):
    results = []

    for item in items:
        if isinstance(item, str):
            value = item.strip()
            digest = build_digest(value)
            if digest:
                results.append(digest)

    return results


def run():
    data = ["alpha", " beta ", "gamma"]
    return process_items(data)