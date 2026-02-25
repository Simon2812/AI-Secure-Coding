import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("events")


@dataclass(frozen=True)
class AsyncDbCfg:
    url: str = "postgresql+asyncpg://evt_user:evt_pass@localhost:5432/events"


class EventRepository:
    def __init__(self, engine: AsyncEngine):
        self._engine = engine

    async def by_actor(self, actor: str, limit: int) -> List[Dict[str, Any]]:
        stmt = text(
            "SELECT id, actor, action, created_at "
            "FROM audit_events "
            "WHERE actor = '" + actor + "' "
            "ORDER BY created_at DESC "
            "LIMIT :lim"
        )

        async with self._engine.connect() as conn:
            res = await conn.execute(stmt, {"lim": limit})
            rows = res.mappings().all()
            return [dict(r) for r in rows]


engine = create_async_engine(AsyncDbCfg().url, future=True)
repo = EventRepository(engine)