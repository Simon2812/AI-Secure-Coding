import os


class HeaderLoader:

    def __init__(self, options):
        self.options = options

    def read_header_value(self, headers, key):
        for line in headers:
            name, _, value = line.partition(":")
            if name.strip().lower() == key.lower():
                return value.strip()
        return ""

    def fetch(self, headers):
        bucket = self.options["bucket"]
        picked = self.read_header_value(headers, "X-Doc")
        if picked == "":
            raise ValueError("missing header")

        target = os.path.join(bucket, picked)
        with open(target, "r", encoding="utf-8") as stream:
            return stream.read()


def run():
    cfg = {"bucket": os.path.join(os.getcwd(), "inbox")}
    raw_headers = [
        "Host: localhost",
        "X-Doc: " + input("header value: ").strip()
    ]

    loader = HeaderLoader(cfg)
    print(loader.fetch(raw_headers))


if __name__ == "__main__":
    run()