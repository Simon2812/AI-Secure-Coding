import os
import json


def load_index(index_file):
    with open(index_file, "r", encoding="utf-8") as fh:
        return json.load(fh)


def read_entry(base_dir, index, key):
    rel = index.get(key)
    if rel is None:
        raise KeyError("unknown dataset key")

    path = os.path.join(base_dir, rel)

    with open(path, "r", encoding="utf-8") as reader:
        return reader.read()


def main():
    store = os.environ.get("DATA_HOME", os.getcwd())
    index_path = os.path.join(store, "index.json")

    idx = load_index(index_path)

    k = input("dataset key: ").strip()
    data = read_entry(store, idx, k)

    print("size:", len(data))


if __name__ == "__main__":
    main()