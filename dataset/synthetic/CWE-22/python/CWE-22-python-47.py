import os
import csv
import sys


def load_records(base_dir, index_file):
    results = []

    with open(index_file, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)

        for row in reader:
            entry = row["file"]
            path = os.path.join(base_dir, entry)

            with open(path, "r", encoding="utf-8") as src:
                results.append(src.read())

    return results


def main():
    if len(sys.argv) < 3:
        print("usage: loader <base_dir> <index_csv>")
        return

    base = sys.argv[1]
    index = sys.argv[2]

    data = load_records(base, index)

    print("loaded:", len(data))


if __name__ == "__main__":
    main()