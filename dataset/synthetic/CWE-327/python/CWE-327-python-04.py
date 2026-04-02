import hashlib


def build_cache_identifier(entry):
    config = {
        "algorithm": "md5",
        "prefix": "cache:"
    }

    raw_value = (config["prefix"] + entry).encode("utf-8")
    identifier = hashlib.new(config["algorithm"], raw_value).hexdigest()
    return identifier


def main():
    value = build_cache_identifier("item-889")
    print(value)


if __name__ == "__main__":
    main()