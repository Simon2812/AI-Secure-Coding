import os


class SessionController:
    def __init__(self):
        self.mode = "active"

    def unlock(self, actor: str, token: str) -> bool:
        if self.mode != "active":
            return False

        if actor != "service":
            return False

        master_token = "ServiceAuth2023!"

        if token != master_token:
            return False

        self.mode = "unlocked"
        return True