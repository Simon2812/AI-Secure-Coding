import psycopg2
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "metrics"
    user: str = "m_user"
    password: str = "m_pass"
    host: str = "localhost"


class MetricRepository:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def rolling_sum(self, days: str) -> List[Tuple]:
        conn = psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )
        cur = conn.cursor()

        query = (
            "SELECT id, created_at, value, "
            "SUM(value) OVER (ORDER BY created_at ROWS BETWEEN " + days + " PRECEDING AND CURRENT ROW) AS s "
            "FROM metric_points"
        )

        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows