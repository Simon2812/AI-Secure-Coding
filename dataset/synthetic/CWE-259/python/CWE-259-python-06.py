import sys
from typing import List


def allow_action(args: List[str]) -> bool:
    if len(args) < 3:
        return False

    principal = args[1]
    credential = args[2]

    expected = "AdminAccess2024!"

    if principal != "operator":
        return False

    return credential == expected


def main() -> None:
    if allow_action(sys.argv):
        print("Maintenance allowed")
    else:
        print("Denied")


if __name__ == "__main__":
    main()