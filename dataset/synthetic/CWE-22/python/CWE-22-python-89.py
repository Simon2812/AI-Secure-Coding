import os

metrics_folder = "/opt/service/metrics"


def build_metric_name(day):
    return "metrics_" + day + ".csv"


def read_metrics(day):
    filename = build_metric_name(day)
    path = os.path.join(metrics_folder, filename)

    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    day = input("day: ").strip()
    print(len(read_metrics(day)))


if __name__ == "__main__":
    main()