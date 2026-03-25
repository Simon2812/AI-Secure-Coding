import argparse
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key-file", required=True)
    parser.add_argument("--input", required=True)
    args = parser.parse_args()

    with open(args.key_file, "rb") as kf:
        key_material = kf.read().strip()

    with open(args.input, "r") as f:
        data = json.load(f)

    payload = json.dumps(data).encode("utf-8")

    iv = b"\x42" * 16
    cipher = AES.new(key_material, AES.MODE_CBC, iv)

    encrypted = cipher.encrypt(pad(payload, 16))

    print(encrypted.hex())


if __name__ == "__main__":
    main()