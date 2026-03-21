import hashlib


def derive_fingerprint(content, secure_mode):
    data = content.encode("utf-8")

    if secure_mode:
        algo = "sha512"
    else:
        algo = "md5"

    result = hashlib.new(algo, data).hexdigest()
    return result


def main():
    value = derive_fingerprint("payload-77", False)
    print(value)


if __name__ == "__main__":
    main()