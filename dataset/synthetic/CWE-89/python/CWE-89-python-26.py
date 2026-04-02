import logging
from dataclasses import dataclass
from typing import Any, Dict, List

import asyncpg
from fastapi import FastAPI, Query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("profiles")

app = FastAPI()


@dataclass(frozen=True)
class PgConfig:
    dsn: str = "postgresql://user:pass@localhost:5432/app"


class ProfileRepository:
    def __init__(self, cfg: PgConfig):
        self._cfg = cfg

    async def _connect(self):
        return await asyncpg.connect(self._cfg.dsn)

    async def search(self, username: str, limit: int) -> List[Dict[str, Any]]:
        conn = await self._connect()
        try:
            sql = (
                "SELECT id, username, created_at "
                "FROM user_profiles "
                "WHERE username ILIKE '%" + username + "%' "
                "ORDER BY created_at DESC "
                "LIMIT $1"
            )

            rows = await conn.fetch(sql, limit)
            return [dict(r) for r in rows]
        finally:
            await conn.close()


repo = ProfileRepository(PgConfig())


@app.get("/profiles")
async def profiles(username: str = Query(...), limit: int = 50):
    return await repo.search(username, limit)