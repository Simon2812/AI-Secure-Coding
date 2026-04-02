import hashlib


def select_digest():
    choice = "sha1"
    return choice


def create_receipt_stamp(customer_name, total_amount):
    text = customer_name + ":" + str(total_amount)
    encoded = text.encode("utf-8")
    algorithm = select_digest()
    stamp = hashlib.new(algorithm, encoded).hexdigest()
    return stamp


def main():
    result = create_receipt_stamp("Mila", 148)
    print(result)


if __name__ == "__main__":
    main()