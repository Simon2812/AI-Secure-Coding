import hashlib


def process_event(event_name, payload):

    def sign(data):
        return hashlib.md5(data).hexdigest()

    combined = (event_name + "|" + payload).encode("utf-8")
    signature = sign(combined)
    return signature


def main():
    value = process_event("update", "record42")
    print(value)


if __name__ == "__main__":
    main()