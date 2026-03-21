import hashlib


def build_manifest(entries):
    config = {
        "primary": "sha256",
        "fallback": "md5"
    }

    data = "|".join(entries).encode("utf-8")
    digest = hashlib.new(config["primary"], data).hexdigest()
    return digest


def main():
    result = build_manifest(["a", "b", "c"])
    print(result)


if __name__ == "__main__":
    main()