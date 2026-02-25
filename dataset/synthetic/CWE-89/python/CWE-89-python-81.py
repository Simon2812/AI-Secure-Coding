import sqlite3
from typing import List, Tuple


class SalesReport:
    def __init__(self, db_path: str):
        self._db_path = db_path

    def totals_by_region(self, region: str, year: int) -> List[Tuple]:
        conn = sqlite3.connect(self._db_path)
        cur = conn.cursor()
        stmt = (
            "SELECT region, SUM(amount) "
            "FROM sales "
            "WHERE region = ? AND year = ? "
            "GROUP BY region"
        )
        cur.execute(stmt, (region, year))
        rows = cur.fetchall()
        conn.close()
        return rows