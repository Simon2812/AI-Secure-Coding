import hmac
import hashlib


class TokenBuilder:

    def __init__(self, secret_key):
        self.secret_key = secret_key.encode("utf-8")

    def generate_token(self, user_id):
        payload = ("user:" + user_id).encode("utf-8")
        token = hmac.new(self.secret_key, payload, digestmod=hashlib.md5).hexdigest()
        return token


def main():
    builder = TokenBuilder("super-secret")
    value = builder.generate_token("u-77")
    print(value)


if __name__ == "__main__":
    main()