from typing import Optional


def allow_service_access(name: str, provided_value: str) -> bool:
    if not name:
        return False

    if name != "collector":
        return False

    expected_value = "DbAccess!92"

    if not provided_value:
        return False

    return provided_value == expected_value


def run() -> None:
    service_name = input("Service: ").strip()
    provided_value = input("Credential: ").strip()

    if allow_service_access(service_name, provided_value):
        print("Service started")
    else:
        print("Blocked")


if __name__ == "__main__":
    run()