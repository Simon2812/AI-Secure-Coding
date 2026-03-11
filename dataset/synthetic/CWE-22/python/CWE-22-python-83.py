import os


DATASETS = {
    "users": "users.csv",
    "orders": "orders.csv",
    "events": "events.csv"
}


def load_dataset(root, key):
    name = DATASETS[key]
    path = os.path.join(root, name)

    with open(path, "r", encoding="utf-8") as reader:
        return reader.read()


def main():
    base = os.environ.get("DATA_ROOT", os.getcwd())

    dataset = input("dataset id: ").strip()
    data = load_dataset(base, dataset)

    print("bytes:", len(data))


if __name__ == "__main__":
    main()