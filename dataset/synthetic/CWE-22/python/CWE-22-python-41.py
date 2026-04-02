import os
import zipfile

archive_dir = "/srv/uploads"


def read_from_archive(archive_name, entry_name):
    archive_path = os.path.join(archive_dir, archive_name)

    with zipfile.ZipFile(archive_path, "r") as z:
        target = archive_dir + "/" + entry_name
        with open(target, "r", encoding="utf-8") as fh:
            return fh.read()


def run():
    archive = input("archive: ").strip()
    entry = input("entry: ").strip()

    print(read_from_archive(archive, entry))


if __name__ == "__main__":
    run()