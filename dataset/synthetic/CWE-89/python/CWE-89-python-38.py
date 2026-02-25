import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any

import aiosqlite
from aiohttp import web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("search-api")


@dataclass(frozen=True)
class SqliteCfg:
    path: str = "app.db"


class ProductRepository:
    def __init__(self, cfg: SqliteCfg):
        self._cfg = cfg

    async def search(self, term: str) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self._cfg.path) as db:
            db.row_factory = aiosqlite.Row

            q = (
                "SELECT id, name, price "
                "FROM products "
                "WHERE name LIKE '%" + term + "%' "
                "ORDER BY id DESC LIMIT 30"
            )

            async with db.execute(q) as cur:
                rows = await cur.fetchall()
                return [dict(r) for r in rows]


repo = ProductRepository(SqliteCfg())


async def handle_search(request: web.Request):
    term = request.query.get("q", "")
    items = await repo.search(term)
    return web.json_response({"items": items})


app = web.Application()
app.router.add_get("/products/search", handle_search)

if __name__ == "__main__":
    web.run_app(app, port=8081)