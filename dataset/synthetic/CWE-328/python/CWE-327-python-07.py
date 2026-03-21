import hashlib


class AuditFormatter:

    def __init__(self):
        self.algorithm = "md5"

    def format_entry(self, action, actor):
        base = action + ":" + actor
        encoded = base.encode("utf-8")
        digest = hashlib.new(self.algorithm, encoded).hexdigest()
        return "AUDIT-" + digest


def main():
    formatter = AuditFormatter()
    value = formatter.format_entry("delete", "user42")
    print(value)


if __name__ == "__main__":
    main()