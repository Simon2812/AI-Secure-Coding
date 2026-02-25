import psycopg2
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "finance"
    user: str = "fin_user"
    password: str = "fin_pass"
    host: str = "localhost"


class RevenueReportService:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def revenue_by_region(
        self,
        year: int,
        min_total: Optional[str]
    ) -> List[Tuple]:

        conn = self._connect()
        cur = conn.cursor()

        base_query = (
            "SELECT region, SUM(amount) AS total "
            "FROM transactions "
            "WHERE EXTRACT(YEAR FROM created_at) = %s "
            "GROUP BY region "
        )

        if min_total:
            base_query += "HAVING SUM(amount) >= " + min_total

        base_query += " ORDER BY total DESC"

        cur.execute(base_query, (year,))
        rows = cur.fetchall()
        conn.close()
        return rows