import os

plugins_dir = "/usr/local/app/plugins"


def resolve_plugin(name):
    if name == "alpha":
        return "alpha.py"
    elif name == "beta":
        return "beta.py"
    elif name == "gamma":
        return "gamma.py"
    else:
        raise KeyError("unknown plugin")


class PluginLoader:

    def load(self, key):
        module = resolve_plugin(key)
        path = os.path.join(plugins_dir, module)

        with open(path, "r", encoding="utf-8") as fh:
            return fh.read()


def main():
    loader = PluginLoader()
    name = input("plugin: ").strip()
    print(len(loader.load(name)))


if __name__ == "__main__":
    main()