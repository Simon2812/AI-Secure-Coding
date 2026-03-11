import os


def refresh_cache(template_name):
    base_dir = os.environ.get("TEMPLATE_DIR", "templates")
    file_path = os.path.join(base_dir, template_name)

    with open(file_path, "r", encoding="utf-8") as reader:
        return reader.read()


def main():
    name = input("template: ").strip()
    data = refresh_cache(name)
    print("size:", len(data))


if __name__ == "__main__":
    main()