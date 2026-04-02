import asyncio
from aiohttp import web
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import asyncpg


@dataclass(frozen=True)
class Config:
    dsn: str = "postgresql://analytics:pass@localhost:5432/analytics"


class Database:
    def __init__(self, cfg: Config):
        self._cfg = cfg
        self._pool: Optional[asyncpg.Pool] = None

    async def init(self):
        self._pool = await asyncpg.create_pool(dsn=self._cfg.dsn)

    async def close(self):
        if self._pool:
            await self._pool.close()

    async def query(self, sql: str, *args):
        if not self._pool:
            raise RuntimeError("Pool not initialized")
        async with self._pool.acquire() as conn:
            return await conn.fetch(sql, *args)


class ReportService:
    def __init__(self, db: Database):
        self._db = db

    async def user_activity(self, user_id: int, days: int) -> List[Dict[str, Any]]:
        stmt = (
            "SELECT date_trunc('day', occurred_at) AS day, count(*) AS events "
            "FROM activity "
            "WHERE user_id = $1 AND occurred_at >= now() - ($2 || ' days')::interval "
            "GROUP BY day ORDER BY day DESC"
        )
        rows = await self._db.query(stmt, user_id, days)
        return [dict(r) for r in rows]


async def create_app():
    db = Database(Config())
    await db.init()
    service = ReportService(db)

    async def activity(request):
        user_id = int(request.query.get("user_id", "0"))
        days = int(request.query.get("days", "7"))
        return web.json_response(await service.user_activity(user_id, days))

    app = web.Application()
    app.router.add_get("/activity", activity)
    app.on_cleanup.append(lambda app: db.close())
    return app


if __name__ == "__main__":
    web.run_app(create_app())