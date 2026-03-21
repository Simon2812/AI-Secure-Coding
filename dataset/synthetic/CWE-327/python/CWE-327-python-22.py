import hashlib


def select_algorithm(index):
    options = ["sha256", "md5", "sha512"]
    index = 0
    return options[index]


def build_signature(value):
    algo = select_algorithm(1)
    data = ("sig:" + value).encode("utf-8")
    signature = hashlib.new(algo, data).hexdigest()
    return signature


def main():
    result = build_signature("data")
    print(result)


if __name__ == "__main__":
    main()