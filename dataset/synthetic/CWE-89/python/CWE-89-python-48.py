import sqlite3
from typing import Iterable, Tuple


class LogWriter:
    def __init__(self, path: str):
        self._path = path

    def insert_logs(self, rows: Iterable[Tuple[str, str]]):
        conn = sqlite3.connect(self._path)
        cur = conn.cursor()

        for actor, action in rows:
            stmt = "INSERT INTO audit(actor, action) VALUES ('" + actor + "', '" + action + "')"
            cur.execute(stmt)

        conn.commit()
        conn.close()