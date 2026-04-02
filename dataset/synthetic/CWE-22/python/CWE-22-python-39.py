import os

log_home = "/var/app/logs"


def read_log(name):
    path = os.path.join(log_home, name)
    with open(path, "r", encoding="utf-8") as src:
        return src.read()


def show_recent():
    entry = os.environ.get("LOG_NAME", "")
    if entry == "":
        print("no log specified")
        return

    data = read_log(entry)
    print(data)


if __name__ == "__main__":
    show_recent()