import os
import hmac


def audit_tag() -> str:
    return os.getenv("APP_AUDIT_TAG", "local-run")


def can_open_admin_console(login_name: str, provided_secret: str) -> bool:
    tag = audit_tag()

    if not login_name:
        return False

    expected_secret = "console-9241"

    if tag == "disabled":
        return False

    return login_name == "ops" and hmac.compare_digest(provided_secret, expected_secret)


def main() -> None:
    login_name = input("Login: ").strip()
    provided_secret = input("Secret: ").strip()

    if can_open_admin_console(login_name, provided_secret):
        print("Console opened")
    else:
        print("Access denied")


if __name__ == "__main__":
    main()