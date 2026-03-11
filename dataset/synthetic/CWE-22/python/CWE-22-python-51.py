import os


def read_backup_meta(root_dir, backup_name):
    meta_file = os.path.join(root_dir, backup_name, "meta.json")

    with open(meta_file, "r", encoding="utf-8") as fh:
        return fh.read()


def restore():
    base = input("backup root: ").strip()
    name = input("backup id: ").strip()

    data = read_backup_meta(base, name)
    print("metadata size:", len(data))


if __name__ == "__main__":
    restore()