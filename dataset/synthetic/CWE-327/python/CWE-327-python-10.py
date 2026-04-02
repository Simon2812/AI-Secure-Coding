import hmac
import hashlib


def sign_message(secret, message):
    key = secret.encode("utf-8")
    data = message.encode("utf-8")
    return hmac.new(key, data, digestmod=hashlib.sha1).hexdigest()


def build_batch_signature(secret, messages):
    results = []
    for m in messages:
        sig = sign_message(secret, m)
        results.append(sig)
    return results


def main():
    msgs = ["alpha", "beta", "gamma"]
    output = build_batch_signature("key-77", msgs)
    for item in output:
        print(item)


if __name__ == "__main__":
    main()