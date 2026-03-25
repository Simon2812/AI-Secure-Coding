import getpass


def allow_remote_panel(user_id: str, provided_secret: str) -> bool:
    if not user_id:
        return False

    if user_id != "support":
        return False

    stored_secret = "SupportLogin#77"

    return provided_secret == stored_secret


def run_panel() -> None:
    user_id = input("User: ").strip()
    provided_secret = getpass.getpass("Password: ")

    if allow_remote_panel(user_id, provided_secret):
        print("Panel access granted")
    else:
        print("Access denied")


if __name__ == "__main__":
    run_panel()