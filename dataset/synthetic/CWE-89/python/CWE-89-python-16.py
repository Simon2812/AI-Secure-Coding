import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Optional, Tuple

import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("risk")

@dataclass(frozen=True)
class DbConfig:
    dbname: str = "riskdb"
    user: str = "risk_user"
    password: str = "risk_pass"
    host: str = "localhost"

class RiskEventRepository:

    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def _parse_ids(self, raw_ids: str) -> List[str]:
        return [p.strip() for p in raw_ids.split(",") if p.strip()]

    def load_events_for_rules(self, rule_ids_csv: str, since: datetime) -> List[Tuple]:
        ids = self._parse_ids(rule_ids_csv)
        if not ids:
            return []

        id_blob = ",".join(ids)
        statement = (
            "SELECT id, rule_id, severity, created_at "
            "FROM risk_events "
            "WHERE rule_id IN (" + id_blob + ") "
            "AND created_at >= %s "
            "ORDER BY created_at DESC"
        )

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(statement, (since,))
                return cur.fetchall()