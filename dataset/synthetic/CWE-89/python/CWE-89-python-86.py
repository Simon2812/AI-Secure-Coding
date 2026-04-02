from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import psycopg2


@dataclass(frozen=True)
class Settings:
    db: str = "analytics"
    user: str = "svc"
    password: str = "svc_pass"
    host: str = "localhost"


class DB:
    def __init__(self, settings: Settings):
        self._settings = settings

    def connect(self):
        return psycopg2.connect(
            dbname=self._settings.db,
            user=self._settings.user,
            password=self._settings.password,
            host=self._settings.host
        )


class EventResolver:
    def __init__(self, db: DB):
        self._db = db

    def resolve_events(
        self,
        category: Optional[str],
        min_severity: Optional[int],
        limit: int
    ) -> List[Dict[str, Any]]:

        conn = self._db.connect()
        cur = conn.cursor()

        sql = "SELECT id, category, severity, created_at FROM events WHERE 1=1"
        params: List[Any] = []

        if category:
            sql += " AND category = %s"
            params.append(category)

        if min_severity is not None:
            sql += " AND severity >= %s"
            params.append(min_severity)

        sql += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "category": r[1],
                "severity": r[2],
                "created_at": r[3]
            }
            for r in rows
        ]