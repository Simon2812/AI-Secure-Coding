import os

catalog_root = "/srv/catalog/files"


def resolve_entry(key):
    value = key
    if value is None:
        raise KeyError("missing entry")

    path = catalog_root + "/" + value
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def run_lookup():
    key = input("lookup key: ").strip()
    result = resolve_entry(key)
    print(result)


if __name__ == "__main__":
    run_lookup()