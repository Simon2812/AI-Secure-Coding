import os


def choose_asset(root):
    names = os.listdir(root)
    picked = input("asset: ").strip()

    if picked not in names:
        raise ValueError("invalid asset")

    file_path = os.path.join(root, picked)

    with open(file_path, "rb") as fh:
        return fh.read()


def main():
    settings = {
        "assets_home": "/var/lib/app/assets"
    }

    base = settings["assets_home"]
    blob = choose_asset(base)

    print(len(blob))


if __name__ == "__main__":
    main()