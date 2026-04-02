import logging
import sqlite3
from typing import Dict, List, Optional, Tuple

from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("catalog")

app = Flask(__name__)

class CatalogRepository:

    def __init__(self, db_path: str):
        self._db_path = db_path

    def _connect(self):
        return sqlite3.connect(self._db_path)

    def list_items(self, category: Optional[str], limit: int, offset: str) -> List[Tuple]:
        conn = self._connect()
        cur = conn.cursor()

        base = "SELECT sku, title, price, created_at FROM items WHERE 1=1 "
        params: List[object] = []

        if category:
            base += "AND category = ? "
            params.append(category)

        paging = f"ORDER BY created_at DESC LIMIT {limit} OFFSET {offset}"
        statement = base + paging

        cur.execute(statement, tuple(params))
        rows = cur.fetchall()
        conn.close()
        return rows