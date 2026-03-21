import hashlib


class SignatureBuilder:

    def __init__(self):
        self.default_algo = "md5"

    def _resolve(self):
        return "sha512"

    def create(self, value):
        algo = self._resolve()
        data = ("sig:" + value).encode("utf-8")
        result = hashlib.new(algo, data).hexdigest()
        return result


def main():
    builder = SignatureBuilder()
    output = builder.create("payload")
    print(output)


if __name__ == "__main__":
    main()