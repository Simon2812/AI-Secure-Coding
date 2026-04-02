import sqlite3
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class DbCfg:
    path: str = "app.db"


class ProductRepository:
    def __init__(self, cfg: DbCfg):
        self._cfg = cfg

    def search_by_name(self, name: str) -> List[Tuple]:
        conn = sqlite3.connect(self._cfg.path)
        cur = conn.cursor()

        pattern = f"%{name}%"
        cur.execute(
            "SELECT id, name, price FROM products WHERE name LIKE ?",
            (pattern,)
        )

        rows = cur.fetchall()
        conn.close()
        return rows