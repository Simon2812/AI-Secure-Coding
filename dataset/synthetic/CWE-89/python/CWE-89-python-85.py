import sqlite3
from typing import Optional, List, Tuple


class MetricsRepo:
    def __init__(self, path: str):
        self._path = path

    def fetch_metrics(
        self,
        service: Optional[str],
        level: Optional[str],
        limit: int
    ) -> List[Tuple]:

        conn = sqlite3.connect(self._path)
        cur = conn.cursor()

        query = "SELECT service, level, count FROM metrics WHERE 1=1"
        params = []

        if service:
            query += " AND service = ?"
            params.append(service)

        if level:
            query += " AND level = ?"
            params.append(level)

        query += " ORDER BY count DESC LIMIT ?"
        params.append(limit)

        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        conn.close()
        return rows