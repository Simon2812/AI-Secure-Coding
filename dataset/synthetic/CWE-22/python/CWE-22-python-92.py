import os
import tempfile


class ConfigReader:

    def __init__(self, base):
        self.base = base

    def load_config(self):
        name = "config.json"
        target_file = os.path.join(self.base, name)

        with open(target_file, "r", encoding="utf-8") as handle:
            return handle.read()


def main():
    root_dir = os.path.join(tempfile.gettempdir(), "app_cfg")

    reader = ConfigReader(root_dir)

    data = reader.load_config()
    print(len(data))


if __name__ == "__main__":
    main()