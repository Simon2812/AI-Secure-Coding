import os


def resolve_dataset(key):
    if key == "users":
        return "users.csv"
    elif key == "orders":
        return "orders.csv"
    elif key == "events":
        return "events.csv"
    else:
        raise KeyError("unknown dataset")


def load_data(root, token):
    name = resolve_dataset(token)
    location = os.path.join(root, name)

    with open(location, "r", encoding="utf-8") as reader:
        return reader.read()


def main():
    settings = {
        "dataset_home": "/var/lib/app/datasets"
    }

    base = settings["dataset_home"]
    key = input("dataset id: ").strip()

    data = load_data(base, key)
    print(len(data))


if __name__ == "__main__":
    main()