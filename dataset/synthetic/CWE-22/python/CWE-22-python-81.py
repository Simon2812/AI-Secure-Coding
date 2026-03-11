import os
import json


index_file = "/data/catalog/index.json"


def load_catalog():
    with open(index_file, "r", encoding="utf-8") as fh:
        return json.load(fh)


def fetch_entry(base_dir, catalog, key):
    entry = catalog.get(key)
    if entry is None:
        raise KeyError("unknown item")

    filename = entry["file"]
    target_path = os.path.join(base_dir, filename)

    with open(target_path, "r", encoding="utf-8") as reader:
        return reader.read()


def main():
    storage_root = "/data/catalog/files"

    catalog = load_catalog()

    item = input("item id: ").strip()
    content = fetch_entry(storage_root, catalog, item)

    print(len(content))


if __name__ == "__main__":
    main()