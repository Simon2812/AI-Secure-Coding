import os

documents_path = "/home/app/docs"


def choose_document(base):
    files = os.listdir(base)
    name = input("document: ").strip()

    if name not in files:
        raise ValueError("invalid document")

    target = os.path.join(base, name)

    with open(target, "r", encoding="utf-8") as handle:
        return handle.read()


def main():
    text = choose_document(documents_path)
    print(text[:80])


if __name__ == "__main__":
    main()