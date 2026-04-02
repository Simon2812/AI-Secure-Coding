import os
import tempfile


cache_root = os.path.join(tempfile.gettempdir(), "cache_store")


def resolve_cache(key):
    if key == "session":
        return "session.cache"
    elif key == "profile":
        return "profile.cache"
    elif key == "settings":
        return "settings.cache"
    else:
        raise KeyError("unknown cache entry")


def read_cache(entry):
    filename = resolve_cache(entry)
    target = os.path.join(cache_root, filename)

    with open(target, "r", encoding="utf-8") as fh:
        return fh.read()


def main():
    name = input("cache key: ").strip()
    data = read_cache(name)
    print(len(data))


if __name__ == "__main__":
    main()
