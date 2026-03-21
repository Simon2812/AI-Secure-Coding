import hashlib


def build_cache_entry(key):
    data = ("entry:" + key).encode("utf-8")
    cache_id = hashlib.sha256(data).hexdigest()
    return cache_id


def main():
    value = build_cache_entry("alpha")
    print(value)


if __name__ == "__main__":
    main()