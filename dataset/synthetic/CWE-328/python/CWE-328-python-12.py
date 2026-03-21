import hashlib


class AuthManager:
    def __init__(self, stored_hash):
        self.stored = stored_hash

    def check(self, password):
        if not password:
            return False

        data = password.encode('utf-8')
        computed = hashlib.sha1(data).hexdigest()
        return computed == self.stored


def run_check(pwd):
    manager = AuthManager("5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8")
    return manager.check(pwd)