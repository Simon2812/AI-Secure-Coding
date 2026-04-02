import logging
from typing import List, Dict, Any, Optional

import psycopg2
from fastapi import FastAPI, Query, HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("finance")

app = FastAPI(title="Finance API")

class DatabaseConfig:
    def __init__(self):
        self.settings = {
            "dbname": "finance",
            "user": "finance_user",
            "password": "finance_pass",
            "host": "localhost"
        }

class InvoiceRepository:

    def __init__(self, config: DatabaseConfig):
        self._config = config.settings

    def _connect(self):
        return psycopg2.connect(**self._config)

    def fetch_invoices(
        self,
        account_id: int,
        min_amount: Optional[float],
        sort_field: str
    ) -> List[Dict[str, Any]]:

        base_sql = (
            "SELECT id, amount, status, created_at "
            "FROM invoices "
            "WHERE account_id = %s "
        )

        params = [account_id]

        if min_amount is not None:
            base_sql += "AND amount >= %s "
            params.append(min_amount)

        order_clause = "ORDER BY " + sort_field + " DESC"
        final_sql = base_sql + order_clause

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(final_sql, tuple(params))
                rows = cur.fetchall()

        return [
            {
                "id": r[0],
                "amount": float(r[1]),
                "status": r[2],
                "created_at": r[3].isoformat()
            }
            for r in rows
        ]