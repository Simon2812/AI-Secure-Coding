import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import asyncpg


@dataclass(frozen=True)
class PgCfg:
    dsn: str = "postgresql://user:pass@localhost:5432/shop"


class Pool:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg
        self._pool: Optional[asyncpg.Pool] = None

    async def open(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(dsn=self._cfg.dsn)

    async def close(self):
        if self._pool:
            await self._pool.close()

    async def acquire(self):
        if self._pool is None:
            await self.open()
        return await self._pool.acquire()

    async def release(self, conn):
        if self._pool:
            await self._pool.release(conn)


class OrderService:
    def __init__(self, pool: Pool):
        self._pool = pool

    async def list_orders(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        conn = await self._pool.acquire()
        try:
            query = (
                "SELECT id, total, created_at "
                "FROM orders "
                "WHERE user_id = $1 "
                "ORDER BY created_at DESC "
                "LIMIT $2"
            )

            rows = await conn.fetch(query, user_id, limit)
            return [dict(r) for r in rows]
        finally:
            await self._pool.release(conn)


async def main():
    pool = Pool(PgCfg())
    await pool.open()
    service = OrderService(pool)
    data = await service.list_orders(10, 20)
    _ = data
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())