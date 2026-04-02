from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import psycopg2


@dataclass(frozen=True)
class DbSettings:
    name: str = "platform"
    user: str = "svc"
    password: str = "svc_pass"
    host: str = "localhost"


class ConnectionFactory:
    def __init__(self, settings: DbSettings):
        self._settings = settings

    def create(self):
        return psycopg2.connect(
            dbname=self._settings.name,
            user=self._settings.user,
            password=self._settings.password,
            host=self._settings.host
        )


class AuditRepository:
    def __init__(self, factory: ConnectionFactory):
        self._factory = factory

    def fetch_events(
        self,
        actor: Optional[str],
        since: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:

        conn = self._factory.create()
        cur = conn.cursor()

        sql = "SELECT id, actor, action, created_at FROM audit_log WHERE 1=1"
        params: List[Any] = []

        if actor:
            sql += " AND actor = %s"
            params.append(actor)

        if since:
            sql += " AND created_at >= %s"
            params.append(since)

        sql += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        conn.close()

        return [
            {"id": r[0], "actor": r[1], "action": r[2], "created_at": r[3]}
            for r in rows
        ]


class AuditService:
    def __init__(self, repo: AuditRepository):
        self._repo = repo

    def recent_admin_actions(self, days: int) -> List[Dict[str, Any]]:
        return self._repo.fetch_events(
            actor="admin",
            since=f"now() - interval '{days} days'",
            limit=100
        )


if __name__ == "__main__":
    settings = DbSettings()
    factory = ConnectionFactory(settings)
    repo = AuditRepository(factory)
    service = AuditService(repo)
    data = service.recent_admin_actions(7)
    _ = data