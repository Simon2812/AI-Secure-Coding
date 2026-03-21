import hashlib
import hmac


def generate_auth_code(secret, message):
    key = secret.encode("utf-8")
    data = message.encode("utf-8")
    code = hmac.new(key, data, digestmod=hashlib.sha512).hexdigest()
    return code


def main():
    result = generate_auth_code("secure-key", "payload-22")
    print(result)


if __name__ == "__main__":
    main()