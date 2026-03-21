import hashlib


def create_receipt_marker(customer_id, total):
    payload = (customer_id + ":" + str(total)).encode("utf-8")
    marker = hashlib.sha256(payload).hexdigest()
    return marker


def main():
    value = create_receipt_marker("cust-104", 87)
    print(value)


if __name__ == "__main__":
    main()