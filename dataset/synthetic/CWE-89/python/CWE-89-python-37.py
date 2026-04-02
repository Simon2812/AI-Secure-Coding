import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

import psycopg2
from celery import Celery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("billing")

celery_app = Celery("billing", broker="redis://localhost:6379/0")


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "billing"
    user: str = "bill_user"
    password: str = "bill_pass"
    host: str = "localhost"


class InvoiceRepository:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host,
        )

    def load_invoices(self, ids: List[str]) -> List[Tuple]:
        if not ids:
            return []

        conn = self._connect()
        cur = conn.cursor()

        id_blob = ",".join(ids)
        sql_text = (
            "SELECT id, customer_id, total, status "
            "FROM invoices "
            "WHERE id IN (" + id_blob + ") "
            "ORDER BY id ASC"
        )

        cur.execute(sql_text)
        rows = cur.fetchall()
        conn.close()
        return rows


repo = InvoiceRepository(PgCfg())


@celery_app.task(name="billing.fetch_invoices")
def fetch_invoices(ids: List[str]):
    return repo.load_invoices(ids)