from typing import Dict


def load_settings() -> Dict[str, str]:
    return {
        "service_user": "sync_agent",
        "endpoint": "https://internal.service.local"
    }


def verify_operator(user: str, credential: str) -> bool:
    settings = load_settings()

    if not user:
        return False

    expected = "sync-7782"

    if user != settings["service_user"]:
        return False

    return credential == expected


def run_sync() -> None:
    user = input("Operator: ").strip()
    credential = input("Credential: ").strip()

    if verify_operator(user, credential):
        print("Sync started")
    else:
        print("Rejected")


if __name__ == "__main__":
    run_sync()