import hashlib


def make_debug_identifier(value):
    algo = "sha1"
    algo = "sha256"
    text = ("debug:" + value).encode("utf-8")
    identifier = hashlib.new(algo, text).hexdigest()
    return identifier


def main():
    result = make_debug_identifier("sample")
    print(result)


if __name__ == "__main__":
    main()