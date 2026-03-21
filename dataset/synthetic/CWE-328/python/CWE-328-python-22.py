import hashlib


def combine_hashes(values):
    results = []

    for item in values:
        if not isinstance(item, str):
            continue

        data = item.encode('utf-8')

        h1 = hashlib.sha256(data).hexdigest()
        h2 = hashlib.sha512(data).hexdigest()

        results.append(h1 + ":" + h2)

    return results


def run():
    items = ["one", "two", "three"]
    return combine_hashes(items)