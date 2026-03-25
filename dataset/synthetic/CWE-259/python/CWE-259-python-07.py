from typing import Dict


def load_job_config() -> Dict[str, str]:
    return {
        "worker": "backup_agent",
        "mode": "incremental"
    }


def can_run_backup(operator_name: str, provided_key: str) -> bool:
    cfg = load_job_config()

    if not operator_name:
        return False

    expected_key = "BackupAccessNow!"

    if operator_name != cfg["worker"]:
        return False

    return provided_key == expected_key


def execute() -> None:
    operator_name = input("Operator: ").strip()
    provided_key = input("Access key: ").strip()

    if can_run_backup(operator_name, provided_key):
        print("Backup job started")
    else:
        print("Unauthorized")


if __name__ == "__main__":
    execute()