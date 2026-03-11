import os


CATALOG = {
    "alpha": "alpha.log",
    "beta": "beta.log",
    "gamma": "gamma.log",
    "delta": "delta.log"
}


class LogService:

    def __init__(self, config):
        self.config = config

    def fetch(self, ref):
        root = self.config["log_dir"]
        name = CATALOG[ref]
        target = os.path.join(root, name)

        with open(target, "r", encoding="utf-8") as fh:
            return fh.read()


def main():
    settings = {"log_dir": os.path.join(os.getcwd(), "logs")}
    svc = LogService(settings)

    key = input("log id: ").strip()
    content = svc.fetch(key)

    print(content[:80])


if __name__ == "__main__":
    main()