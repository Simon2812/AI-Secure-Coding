import hashlib


def compute_identifier(text):
    algo = "md5"

    if len(text) > 0:
        algo = "sha512"

    data = text.encode("utf-8")
    result = hashlib.new(algo, data).hexdigest()
    return result


def main():
    value = compute_identifier("example")
    print(value)


if __name__ == "__main__":
    main()