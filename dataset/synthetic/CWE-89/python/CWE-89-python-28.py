import sqlite3
from typing import List, Tuple


class ReportTool:
    def __init__(self, db_path: str):
        self._db_path = db_path

    def find_by_status(self, status: str) -> List[Tuple]:
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()

        query = (
            "SELECT id, name, status "
            "FROM jobs "
            "WHERE status = '" + status + "'"
        )

        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows