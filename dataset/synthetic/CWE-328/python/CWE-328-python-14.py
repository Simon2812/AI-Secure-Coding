import hashlib


class TokenStore:
    def __init__(self):
        self.tokens = []

    def add(self, raw):
        if not raw:
            return

        data = raw.encode('utf-8')
        digest = hashlib.sha1(data).hexdigest()
        self.tokens.append(digest)


def process_batch(values):
    store = TokenStore()

    for item in values:
        if isinstance(item, str):
            store.add(item.strip())

    return store.tokens