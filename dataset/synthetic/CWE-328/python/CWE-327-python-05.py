import hashlib


def resolve_algorithm(flag):
    if flag:
        return "sha1"
    else:
        return "sha256"


def calculate_file_fingerprint(path, use_fast_mode):
    with open(path, "rb") as f:
        content = f.read()

    algo = resolve_algorithm(use_fast_mode)
    fingerprint = hashlib.new(algo, content).hexdigest()
    return fingerprint


def main():
    name = "sample.txt"
    result = calculate_file_fingerprint(name, True)
    print(result)


if __name__ == "__main__":
    main()