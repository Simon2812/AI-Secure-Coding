import hashlib


def compute_record_checksum(records):
    result = []
    for record in records:
        data = (record["id"] + "|" + record["value"]).encode("utf-8")
        checksum = hashlib.sha1(data).hexdigest()
        result.append(checksum)
    return result


def main():
    dataset = [
        {"id": "r1", "value": "alpha"},
        {"id": "r2", "value": "beta"}
    ]
    output = compute_record_checksum(dataset)
    for item in output:
        print(item)


if __name__ == "__main__":
    main()