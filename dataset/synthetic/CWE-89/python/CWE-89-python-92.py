from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import psycopg2
from psycopg2 import sql


@dataclass(frozen=True)
class DbConfig:
    dbname: str = "reporting"
    user: str = "svc"
    password: str = "svc_pass"
    host: str = "localhost"


class ConnectionManager:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def open(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )


class ReportRepository:
    def __init__(self, manager: ConnectionManager):
        self._manager = manager

    def list_reports(
        self,
        owner: Optional[str],
        min_score: Optional[int],
        limit: int
    ) -> List[Dict[str, Any]]:

        conn = self._manager.open()
        cur = conn.cursor()

        base = "SELECT id, owner, score, created_at FROM reports WHERE 1=1"
        params: List[Any] = []

        if owner:
            base += " AND owner = %s"
            params.append(owner)

        if min_score is not None:
            base += " AND score >= %s"
            params.append(min_score)

        base += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        cur.execute(base, tuple(params))
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "owner": r[1],
                "score": r[2],
                "created_at": r[3]
            }
            for r in rows
        ]


class ReportService:
    def __init__(self, repo: ReportRepository):
        self._repo = repo

    def top_reports(self, owner: Optional[str]) -> List[Dict[str, Any]]:
        return self._repo.list_reports(owner=owner, min_score=50, limit=100)


if __name__ == "__main__":
    cfg = DbConfig()
    manager = ConnectionManager(cfg)
    repo = ReportRepository(manager)
    service = ReportService(repo)
    data = service.top_reports(owner="admin")
    _ = data