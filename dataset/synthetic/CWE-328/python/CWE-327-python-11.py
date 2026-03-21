import hashlib
import sys


def build_document_proof(name):
    data = ("doc:" + name).encode("utf-8")
    proof = hashlib.new("md4", data).hexdigest()
    return proof


def main():
    arg = "fileA"
    if len(sys.argv) > 1:
        arg = sys.argv[1]

    result = build_document_proof(arg)
    print(result)


if __name__ == "__main__":
    main()