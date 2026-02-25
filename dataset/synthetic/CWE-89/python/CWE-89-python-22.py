import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("metrics")


@dataclass(frozen=True)
class MetricsConfig:
    url: str = "postgresql+psycopg2://metrics_user:metrics_pass@localhost:5432/metrics"


def build_engine(cfg: MetricsConfig) -> Engine:
    return create_engine(cfg.url, pool_pre_ping=True, future=True)


class MetricsRepository:

    def __init__(self, engine: Engine):
        self._engine = engine

    def top_pages(self, day: str, sort_field: str) -> List[Dict[str, Any]]:
        direction = "DESC"

        # Vulnerable: sort_field interpolated into ORDER BY
        order_sql = " ORDER BY " + sort_field + " " + direction

        stmt = text(
            "SELECT path, views, uniques "
            "FROM page_metrics "
            "WHERE day = :day" + order_sql +
            " LIMIT 100"
        )

        with self._engine.connect() as conn:
            rows = conn.execute(stmt, {"day": day}).fetchall()

        return [{"path": r[0], "views": int(r[1]), "uniques": int(r[2])} for r in rows]


class MetricsService:

    def __init__(self):
        self.repo = MetricsRepository(build_engine(MetricsConfig()))

    def report(self, day: str, sort_field: str):
        return self.repo.top_pages(day, sort_field)