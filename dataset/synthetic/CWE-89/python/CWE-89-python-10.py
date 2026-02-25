import json
import logging
import psycopg2
from dataclasses import dataclass
from typing import List, Optional, Tuple

logging.basicConfig(level=logging.INFO)

@dataclass(frozen=True)
class DbConfig:
    dbname: str
    user: str
    password: str
    host: str = "localhost"

def load_config(path: str) -> DbConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return DbConfig(
        dbname=raw.get("dbname", "analytics"),
        user=raw.get("user", "analytics_user"),
        password=raw.get("password", "analytics_pass"),
        host=raw.get("host", "localhost"),
    )

class AnalyticsRepository:

    def __init__(self, cfg: DbConfig):
        self._cfg = cfg
        self._conn = psycopg2.connect(
            dbname=cfg.dbname,
            user=cfg.user,
            password=cfg.password,
            host=cfg.host
        )

    def close(self) -> None:
        self._conn.close()

    def _cursor(self):
        return self._conn.cursor()

    def fetch_events(self, actor: str, event_type: Optional[str]) -> List[Tuple]:
        cur = self._cursor()

        base_query = "SELECT id, actor, kind, created_at FROM audit_events WHERE actor = '" + actor + "'"

        if event_type:
            base_query += " AND kind = '" + event_type + "'"

        base_query += " ORDER BY created_at DESC"

        cur.execute(base_query)
        return cur.fetchall()

class ReportService:

    def __init__(self, repo: AnalyticsRepository):
        self._repo = repo

    def print_recent(self, actor: str, kind: Optional[str] = None, limit: int = 10) -> None:
        items = self._repo.fetch_events(actor, kind)
        for row in items[:limit]:
            logging.info("event id=%s actor=%s kind=%s at=%s", row[0], row[1], row[2], row[3])

def run_report(config_path: str, actor: str, kind: Optional[str]) -> None:
    cfg = load_config(config_path)
    repo = AnalyticsRepository(cfg)
    try:
        ReportService(repo).print_recent(actor, kind)
    finally:
        repo.close()