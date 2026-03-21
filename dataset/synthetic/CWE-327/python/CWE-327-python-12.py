import hashlib


class ManifestBuilder:

    def build_marker(self, name, version):
        raw = (name + "#" + version).encode("utf-8")
        algo = "ripemd160"
        marker = hashlib.new(algo, raw).hexdigest()
        return marker


def main():
    builder = ManifestBuilder()
    value = builder.build_marker("pkg", "1.2")
    print(value)


if __name__ == "__main__":
    main()