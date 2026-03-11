import os

settings = {
    "artifact_home": "/var/lib/app/artifacts"
}


def resolve_name(key):
    if key == "build":
        return "build.bin"
    elif key == "snapshot":
        return "snapshot.bin"
    elif key == "release":
        return "release.bin"
    else:
        raise KeyError("unknown artifact")


def read_blob(config, token):
    root = config["artifact_home"]
    filename = resolve_name(token)
    location = os.path.join(root, filename)

    with open(location, "rb") as src:
        return src.read()


def main():
    key = input("artifact id: ").strip()
    data = read_blob(settings, key)
    print(len(data))


if __name__ == "__main__":
    main()