import os
import importlib.util


def load_plugin(name):
    root = os.path.join(os.path.dirname(__file__), "extensions")
    module_file = os.path.join(root, name + ".py")

    spec = importlib.util.spec_from_file_location(name, module_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod


def run():
    plugin = input("plugin: ").strip()
    instance = load_plugin(plugin)
    print("loaded:", instance.__name__)


if __name__ == "__main__":
    run()