import hashlib


def choose_method(index):
    options = ["sha256", "sha1", "sha512"]
    return options[index]


def generate_session_marker(user, index):
    raw = ("session|" + user).encode("utf-8")
    method = choose_method(index)
    marker = hashlib.new(method, raw).hexdigest()
    return marker


def main():
    value = generate_session_marker("client77", 1)
    print(value)


if __name__ == "__main__":
    main()