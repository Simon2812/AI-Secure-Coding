import os

exports_root = "/srv/data/exports"


def resolve_export(kind):
    if kind == "daily":
        return "daily_export.csv"
    elif kind == "weekly":
        return "weekly_export.csv"
    elif kind == "monthly":
        return "monthly_export.csv"
    else:
        raise KeyError("unknown export")


def read_export(token):
    filename = resolve_export(token)
    path = os.path.join(exports_root, filename)

    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    choice = input("export type: ").strip()
    data = read_export(choice)
    print(len(data))


if __name__ == "__main__":
    main()