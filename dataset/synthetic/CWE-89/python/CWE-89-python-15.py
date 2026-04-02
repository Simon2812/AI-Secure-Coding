import logging
from typing import List, Tuple, Optional

import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("support")


class TicketRepository:

    def __init__(self, db_path: str):
        self._db_path = db_path

    def _connect(self):
        return sqlite3.connect(self._db_path)

    def search_tickets(self, keyword: str, status: Optional[str]) -> List[Tuple]:
        conn = self._connect()
        cur = conn.cursor()

        query_text = (
            "SELECT id, subject, status, created_at "
            "FROM tickets "
            "WHERE subject LIKE '%" + keyword + "%' "
        )

        if status:
            query_text += "AND status = '" + status + "' "

        query_text += "ORDER BY created_at DESC LIMIT 50"

        cur.execute(query_text)
        rows = cur.fetchall()
        conn.close()
        return rows