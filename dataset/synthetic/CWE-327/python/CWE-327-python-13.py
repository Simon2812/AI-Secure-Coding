import hashlib
import hmac


def normalize(value):
    return value.strip().lower()


def sign_request(secret, route):
    prepared = normalize(route).encode("utf-8")
    key = secret.encode("utf-8")
    signature = hmac.new(key, prepared, digestmod=hashlib.md4).hexdigest()
    return signature


def main():
    result = sign_request("k-991", "/API/Update")
    print(result)


if __name__ == "__main__":
    main()