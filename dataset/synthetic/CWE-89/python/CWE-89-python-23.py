import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cleanup")


@dataclass(frozen=True)
class CleanupConfig:
    db_path: str = "appdata.db"


class CleanupRepository:

    def __init__(self, cfg: CleanupConfig):
        self._cfg = cfg

    def _connect(self):
        return sqlite3.connect(self._cfg.db_path)

    def purge_sessions(self, before_iso: str, status: str) -> int:
        conn = self._connect()
        cur = conn.cursor()

        # Vulnerable: status concatenated into SQL script executed as a script
        script = (
            "DELETE FROM sessions "
            "WHERE last_seen < '" + before_iso + "' "
            "AND status = '" + status + "';"
        )

        cur.executescript(script)
        conn.commit()
        affected = cur.rowcount
        conn.close()
        return affected


class CleanupJob:

    def __init__(self):
        self.repo = CleanupRepository(CleanupConfig())

    def run(self, before_iso: str, status: str):
        removed = self.repo.purge_sessions(before_iso, status)
        logger.info("removed=%d status=%s", removed, status)