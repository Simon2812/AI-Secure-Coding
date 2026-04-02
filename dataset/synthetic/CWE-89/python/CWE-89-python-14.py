import logging
from typing import List, Tuple

import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("analytics")


class AnalyticsRepository:

    def __init__(self):
        self._dsn = dict(
            dbname="analytics",
            user="analytics_user",
            password="analytics_pass",
            host="localhost"
        )

    def _connect(self):
        return psycopg2.connect(**self._dsn)

    def aggregate_events(self, start_date: str, end_date: str, group_field: str) -> List[Tuple]:

        base = (
            "SELECT " + group_field + ", COUNT(*) "
            "FROM audit_events "
            "WHERE created_at >= %s AND created_at <= %s "
            "GROUP BY " + group_field + " "
            "ORDER BY COUNT(*) DESC"
        )

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(base, (start_date, end_date))
                return cur.fetchall()