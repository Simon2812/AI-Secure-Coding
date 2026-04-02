from pathlib import Path

config_home = Path("/etc/app/configs")


class ConfigService:

    def __init__(self, base):
        self.base = base

    def read_config(self, key):
        location = self.base / key
        with open(location, "r", encoding="utf-8") as handle:
            return handle.read()


def execute():
    svc = ConfigService(config_home)
    name = input("config key: ").strip()
    content = svc.read_config(name)
    print(content)


if __name__ == "__main__":
    execute()