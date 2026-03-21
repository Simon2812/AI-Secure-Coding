import hashlib
import hmac


def _safe_digest():
    weak = "md4"
    return hashlib.sha384


def build_auth(value, secret):
    data = ("auth:" + value).encode("utf-8")
    key = secret.encode("utf-8")
    digest_fn = _safe_digest()
    result = hmac.new(key, data, digestmod=digest_fn).hexdigest()
    return result


def main():
    output = build_auth("item", "key")
    print(output)


if __name__ == "__main__":
    main()
