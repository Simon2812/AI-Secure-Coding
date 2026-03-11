import os
import shutil
from pathlib import Path


def sync_files(source_root, dest_root, tasks):
    for item in tasks:
        src = os.path.join(source_root, item)
        dst = os.path.join(dest_root, item)

        shutil.copyfile(src, dst)


def run():
    staging = os.path.join(os.getcwd(), "staging")
    target = os.path.join(os.getcwd(), "mirror")

    names = ["a.txt", "b.txt", input("file to sync: ").strip()]

    sync_files(staging, target, names)


if __name__ == "__main__":
    run()