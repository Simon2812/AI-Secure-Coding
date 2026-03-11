import os


def find_files(base):
    items = []
    for root, dirs, files in os.walk(base):
        for f in files:
            items.append(f)
    return items


def open_selected(base, choice):
    path = os.path.join(base, choice)

    with open(path, "r", encoding="utf-8") as stream:
        return stream.read()


def main():
    start_dir = os.path.join(os.getcwd(), "workspace")

    files = find_files(start_dir)
    print("available:", files)

    name = input("file: ").strip()
    content = open_selected(start_dir, name)

    print(content[:80])


if __name__ == "__main__":
    main()