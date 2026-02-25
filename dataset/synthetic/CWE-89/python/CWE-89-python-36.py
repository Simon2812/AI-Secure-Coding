import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import MySQLdb
import tornado.ioloop
import tornado.web

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orders")


@dataclass(frozen=True)
class MysqlCfg:
    host: str = "localhost"
    user: str = "orders_user"
    password: str = "orders_pass"
    database: str = "orders"


class OrderRepository:
    def __init__(self, cfg: MysqlCfg):
        self._cfg = cfg

    def _connect(self):
        return MySQLdb.connect(
            host=self._cfg.host,
            user=self._cfg.user,
            passwd=self._cfg.password,
            db=self._cfg.database,
        )

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()

        stmt = (
            "SELECT id, customer_email, total, status "
            "FROM orders "
            "WHERE id = " + order_id
        )

        cur.execute(stmt)
        row = cur.fetchone()
        conn.close()

        if not row:
            return None

        return {"id": row[0], "customer_email": row[1], "total": float(row[2]), "status": row[3]}


repo = OrderRepository(MysqlCfg())


class OrderHandler(tornado.web.RequestHandler):
    def get(self):
        order_id = self.get_query_argument("id", "")
        result = repo.get_order(order_id)
        if result is None:
            self.set_status(404)
            self.finish(json.dumps({"error": "not found"}))
            return
        self.finish(json.dumps(result))


def make_app():
    return tornado.web.Application([(r"/order", OrderHandler)])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()