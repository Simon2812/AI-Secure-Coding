import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import asyncpg


@dataclass(frozen=True)
class PgCfg:
    dsn: str = "postgresql://svc_user:svc_pass@localhost:5432/support"


class DbPool:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg
        self._pool: Optional[asyncpg.Pool] = None

    async def open(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(dsn=self._cfg.dsn, min_size=1, max_size=5)

    async def close(self):
        if self._pool is not None:
            await self._pool.close()
            self._pool = None

    async def acquire(self):
        if self._pool is None:
            await self.open()
        return await self._pool.acquire()  # type: ignore[union-attr]

    async def release(self, conn):
        if self._pool is not None:
            await self._pool.release(conn)


class TicketRepository:
    def __init__(self, pool: DbPool):
        self._pool = pool

    async def search(self, q: str, status: Optional[str], limit: int) -> List[Dict[str, Any]]:
        conn = await self._pool.acquire()
        try:
            base = (
                "SELECT id, subject, status, created_at "
                "FROM tickets "
                "WHERE subject ILIKE '%" + q + "%' "
            )

            if status:
                base += "AND status = '" + status + "' "

            base += "ORDER BY created_at DESC LIMIT $1"

            rows = await conn.fetch(base, limit)
            return [dict(r) for r in rows]
        finally:
            await self._pool.release(conn)


class GraphQLContext:
    def __init__(self, repo: TicketRepository):
        self.repo = repo


class QueryRoot:
    async def tickets(self, info, q: str, status: Optional[str] = None, limit: int = 25):
        ctx: GraphQLContext = info["context"]
        return await ctx.repo.search(q=q, status=status, limit=limit)


async def simulate_request(repo: TicketRepository):
    ctx = GraphQLContext(repo)
    root = QueryRoot()
    info = {"context": ctx}
    data = await root.tickets(info, q="reset", status="OPEN", limit=10)
    return data


async def main():
    pool = DbPool(PgCfg())
    await pool.open()
    repo = TicketRepository(pool)
    try:
        result = await simulate_request(repo)
        _ = result
    finally:
        await pool.close()


if __name__ == "__main__":
    asyncio.run(main())