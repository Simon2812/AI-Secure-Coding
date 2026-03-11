import os

dataset_store = "/opt/data/datasets"


def map_dataset(key):
    if key == "users":
        return "users.csv"
    elif key == "orders":
        return "orders.csv"
    elif key == "events":
        return "events.csv"
    else:
        raise KeyError("unknown dataset")


def load_dataset(name):
    filename = map_dataset(name)
    file_path = os.path.join(dataset_store, filename)

    with open(file_path, "r", encoding="utf-8") as reader:
        return reader.read()


def main():
    key = input("dataset: ").strip()
    data = load_dataset(key)
    print(len(data))


if __name__ == "__main__":
    main()