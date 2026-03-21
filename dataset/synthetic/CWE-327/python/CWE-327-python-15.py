import hashlib


def transform(parts):
    return [p.upper() for p in parts]


def build_artifact_signature(parts):
    normalized = transform(parts)
    combined = "|".join(normalized).encode("utf-8")
    signature = hashlib.new("sha1", combined).hexdigest()
    return signature


def main():
    data = ["aa", "bb", "cc"]
    result = build_artifact_signature(data)
    print(result)


if __name__ == "__main__":
    main()