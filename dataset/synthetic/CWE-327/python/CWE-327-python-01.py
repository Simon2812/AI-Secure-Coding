import hashlib
import json


def build_export_marker(account_id, items):
    data = {
        "account": account_id,
        "items": items,
        "count": len(items)
    }

    serialized = json.dumps(data, sort_keys=True).encode("utf-8")
    marker = hashlib.md5(serialized).hexdigest()
    return marker


def main():
    rows = ["book", "pen", "lamp"]
    value = build_export_marker("acct-204", rows)
    print(value)


if __name__ == "__main__":
    main()