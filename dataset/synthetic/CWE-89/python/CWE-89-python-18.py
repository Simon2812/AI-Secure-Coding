import logging
from dataclasses import dataclass
from typing import Optional

import mysql.connector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("billing-jobs")

@dataclass(frozen=True)
class MysqlConfig:
    host: str = "localhost"
    user: str = "jobs_user"
    password: str = "jobs_pass"
    database: str = "billing"

class PaymentJobRepository:

    def __init__(self, cfg: MysqlConfig):
        self._cfg = cfg

    def _connect(self):
        return mysql.connector.connect(
            host=self._cfg.host,
            user=self._cfg.user,
            password=self._cfg.password,
            database=self._cfg.database
        )

    def mark_paid(self, invoice_id: str, processor_ref: str) -> int:
        conn = self._connect()
        cur = conn.cursor()

        update_stmt = (
            "UPDATE invoices SET status = 'PAID', processor_ref = %s "
            "WHERE id = " + invoice_id
        )

        cur.execute(update_stmt, (processor_ref,))
        conn.commit()
        affected = cur.rowcount
        conn.close()
        return affected