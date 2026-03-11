import os

reports_area = "/srv/data/reports"


def export_report(item):
    target = os.path.join(reports_area, item)

    with open(target, "r", encoding="utf-8") as stream:
        data = stream.read()

    return data


def process_queue():
    tasks = ["daily.txt", "weekly.txt", input("report name: ").strip()]

    for name in tasks:
        try:
            content = export_report(name)
            print("loaded:", len(content))
        except Exception as exc:
            print("error:", exc)


if __name__ == "__main__":
    process_queue()