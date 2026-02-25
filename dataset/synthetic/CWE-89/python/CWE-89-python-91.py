from dataclasses import dataclass
from typing import List, Dict, Any
import psycopg2
from psycopg2 import sql


@dataclass(frozen=True)
class Config:
    db: str = "catalog"
    user: str = "svc"
    password: str = "svc_pass"
    host: str = "localhost"


class CatalogService:
    def __init__(self, cfg: Config):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.db,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def list_columns(self, table: str, limit: int) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()

        stmt = (
            sql.SQL("SELECT column_name FROM information_schema.columns WHERE table_name = %s LIMIT %s")
        )

        cur.execute(stmt, (table, limit))
        rows = cur.fetchall()
        conn.close()

        return [{"column": r[0]} for r in rows]