import pyodbc
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class SqlServerCfg:
    conn_str: str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=inventory;"
        "UID=inv_user;"
        "PWD=inv_pass"
    )


class InventoryService:
    def __init__(self, cfg: SqlServerCfg):
        self._cfg = cfg

    def list_items(self, sort_direction: str) -> List[Tuple]:
        conn = pyodbc.connect(self._cfg.conn_str)
        cur = conn.cursor()

        query = (
            "SELECT id, name, quantity "
            "FROM stock "
            "ORDER BY quantity " + sort_direction
        )

        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows