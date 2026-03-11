import os

BASE_STORAGE = "/opt/app/storage"


def preview_file(identifier):
    location = os.path.join(BASE_STORAGE, identifier)
    with open(location, "r", encoding="utf-8") as reader:
        return reader.readline()


def run_preview():
    value = input("Enter file id: ").strip()
    result = preview_file(value)
    print(result)


if __name__ == "__main__":
    run_preview()