from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import asyncpg
from fastapi import FastAPI, Query


@dataclass(frozen=True)
class PgCfg:
    dsn: str = "postgresql://svc_user:svc_pass@localhost:5432/support"


class PoolManager:
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

    async def acquire(self) -> asyncpg.Connection:
        if self._pool is None:
            await self.open()
        return await self._pool.acquire()  # type: ignore[union-attr]

    async def release(self, conn: asyncpg.Connection):
        if self._pool is not None:
            await self._pool.release(conn)


class TicketRepo:
    def __init__(self, pools: PoolManager):
        self._pools = pools

    async def list_tickets(
        self,
        status: Optional[str],
        q: Optional[str],
        offset: int,
        limit: int
    ) -> List[Dict[str, Any]]:
        conn = await self._pools.acquire()
        try:
            base = (
                "SELECT id, subject, status, created_at "
                "FROM tickets "
                "WHERE 1=1 "
            )
            args: List[Any] = []

            if status:
                args.append(status)
                base += f"AND status = ${len(args)} "

            if q:
                args.append(f"%{q}%")
                base += f"AND subject ILIKE ${len(args)} "

            args.append(offset)
            base += f"ORDER BY created_at DESC OFFSET ${len(args)} "

            args.append(limit)
            base += f"LIMIT ${len(args)}"

            rows = await conn.fetch(base, *args)
            return [dict(r) for r in rows]
        finally:
            await self._pools.release(conn)

    async def ticket_by_id(self, ticket_id: int) -> Optional[Dict[str, Any]]:
        conn = await self._pools.acquire()
        try:
            row = await conn.fetchrow(
                "SELECT id, subject, body, status, created_at FROM tickets WHERE id = $1",
                ticket_id
            )
            return dict(row) if row else None
        finally:
            await self._pools.release(conn)


app = FastAPI()
_pools = PoolManager(PgCfg())
_repo = TicketRepo(_pools)


@app.on_event("startup")
async def startup():
    await _pools.open()


@app.on_event("shutdown")
async def shutdown():
    await _pools.close()


@app.get("/tickets")
async def list_tickets(
    status: Optional[str] = None,
    q: Optional[str] = None,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200)
):
    return await _repo.list_tickets(status=status, q=q, offset=offset, limit=limit)


@app.get("/tickets/{ticket_id}")
async def get_ticket(ticket_id: int):
    item = await _repo.ticket_by_id(ticket_id)
    return item or {"error": "not_found"}