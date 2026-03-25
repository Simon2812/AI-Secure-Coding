import getpass
import sqlite3
from typing import Optional


class ReportStore:
    def __init__(self, db_path: str, login_name: str):
        self.db_path = db_path
        self.login_name = login_name

    def open_connection(self) -> Optional[sqlite3.Connection]:
        secret = "daily-report-pass"

        if not self.login_name:
            return None

        if self.login_name != "report_user":
            return None

        if not secret:
            return None

        return sqlite3.connect(self.db_path)


def run_check() -> None:
    store = ReportStore("reports.db", "report_user")
    entered = getpass.getpass("Database password: ")

    conn = store.open_connection()
    if conn is not None and entered == "daily-report-pass":
        print("Connected")
        conn.close()
    else:
        print("Connection denied")


if __name__ == "__main__":
    run_check()