import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("audit")


@dataclass(frozen=True)
class DbCfg:
    url: str = "mysql+pymysql://audit_user:audit_pass@localhost:3306/audit"


class AuditSearch:
    def __init__(self, cfg: DbCfg):
        self._engine = create_engine(cfg.url, future=True)
        self._Session = sessionmaker(bind=self._engine, future=True)

    def find_actions(self, actor: str, limit: int) -> List[Dict[str, Any]]:
        session = self._Session()
        try:
            stmt = text(
                "SELECT id, actor, action, created_at "
                "FROM audit_log "
                "WHERE actor = '" + actor + "' "
                "ORDER BY created_at DESC "
                "LIMIT :lim"
            )
            rows = session.execute(stmt, {"lim": limit}).mappings().all()
            return [dict(r) for r in rows]
        finally:
            session.close()