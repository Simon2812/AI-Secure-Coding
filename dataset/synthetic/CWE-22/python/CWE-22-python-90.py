import os

cache_dir = "/var/tmp/app_cache"


class CacheReader:

    def resolve(self, name):
        if name == "session":
            return "session.cache"
        elif name == "profile":
            return "profile.cache"
        elif name == "prefs":
            return "prefs.cache"
        else:
            raise KeyError("unknown cache")

    def read(self, key):
        filename = self.resolve(key)
        target = os.path.join(cache_dir, filename)

        with open(target, "r", encoding="utf-8") as fh:
            return fh.read()


def main():
    reader = CacheReader()
    key = input("cache key: ").strip()
    print(len(reader.read(key)))


if __name__ == "__main__":
    main()