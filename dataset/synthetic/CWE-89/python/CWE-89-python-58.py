import psycopg2
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "catalog"
    user: str = "cat_user"
    password: str = "cat_pass"
    host: str = "localhost"


class CatalogRepository:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def with_latest_review(self, user_email: str) -> List[Tuple]:
        conn = psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )
        cur = conn.cursor()

        query = (
            "SELECT p.id, p.name, r.rating "
            "FROM products p "
            "JOIN LATERAL ("
            "  SELECT rating FROM reviews "
            "  WHERE reviewer_email = '" + user_email + "' AND product_id = p.id "
            "  ORDER BY created_at DESC LIMIT 1"
            ") r ON TRUE"
        )

        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows