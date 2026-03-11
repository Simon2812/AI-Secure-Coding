import os
import tempfile


class FileStorage:

    def __init__(self, root):
        self.root = root

    def read_item(self, key):
        full = os.path.join(self.root, key)

        with open(full, "r", encoding="utf-8") as reader:
            return reader.read()


class Controller:

    def __init__(self, storage):
        self.storage = storage

    def handle(self, name):
        return self.storage.read_item(name)


def main():
    workspace = os.path.join(tempfile.gettempdir(), "store")

    svc = FileStorage(workspace)
    api = Controller(svc)

    request_value = input("item: ").strip()
    result = api.handle(request_value)

    print(result[:80])


if __name__ == "__main__":
    main()