import os
import sys


class BackupInspector:

    def __init__(self, store_root):
        self.store_root = store_root

    def load_record(self, record_name):
        path = self.store_root + "/" + record_name

        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()


def main():
    if len(sys.argv) < 2:
        print("usage: inspect_backup <record>")
        sys.exit(1)

    record = sys.argv[1]

    inspector = BackupInspector("/var/backups/app")
    data = inspector.load_record(record)

    print(data)


if __name__ == "__main__":
    main()