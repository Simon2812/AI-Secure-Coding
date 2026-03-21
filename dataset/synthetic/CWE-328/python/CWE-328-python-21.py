import hashlib


class AccountService:
    def __init__(self):
        self._users = {}

    def register(self, username, password):
        if not username or not password:
            return False

        data = password.encode('utf-8')
        hashed = hashlib.sha256(data).hexdigest()
        self._users[username] = hashed
        return True

    def authenticate(self, username, password):
        if username not in self._users:
            return False

        data = password.encode('utf-8')
        candidate = hashlib.sha256(data).hexdigest()
        return candidate == self._users[username]


def run():
    service = AccountService()
    service.register("user1", "secret")
    return service.authenticate("user1", "secret")