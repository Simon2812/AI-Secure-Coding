import os


settings = {
    "artifact_home": "/var/lib/app/artifacts"
}


class ArtifactReader:

    def __init__(self, cfg):
        self.cfg = cfg

    def load(self, token):
        base = self.cfg["artifact_home"]
        location = os.path.join(base, token)

        with open(location, "rb") as fp:
            return fp.read()


def start():
    reader = ArtifactReader(settings)
    key = input("artifact: ").strip()
    blob = reader.load(key)
    print("bytes:", len(blob))


if __name__ == "__main__":
    start()