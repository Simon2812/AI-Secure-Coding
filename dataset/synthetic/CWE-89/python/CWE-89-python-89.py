from fastapi import FastAPI, Query
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import psycopg2


@dataclass(frozen=True)
class Config:
    db: str = "orders"
    user: str = "svc"
    password: str = "svc_pass"
    host: str = "localhost"


class Repo:
    def __init__(self, cfg: Config):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.db,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def list_orders(
        self,
        customer: Optional[str],
        status: Optional[str],
        min_total: Optional[int],
        limit: int
    ) -> List[Dict[str, Any]]:

        conn = self._connect()
        cur = conn.cursor()

        sql = "SELECT id, customer, status, total FROM orders WHERE 1=1"
        params: List[Any] = []

        if customer:
            sql += " AND customer = %s"
            params.append(customer)

        if status:
            sql += " AND status = %s"
            params.append(status)

        if min_total is not None:
            sql += " AND total >= %s"
            params.append(min_total)

        sql += " ORDER BY id DESC LIMIT %s"
        params.append(limit)

        cur.execute(sql, tuple(params))
        rows = cur.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "customer": r[1],
                "status": r[2],
                "total": r[3]
            }
            for r in rows
        ]


app = FastAPI()
_repo = Repo(Config())


@app.get("/orders")
def orders(
    customer: Optional[str] = None,
    status: Optional[str] = None,
    min_total: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200)
):
    return _repo.list_orders(customer, status, min_total, limit)