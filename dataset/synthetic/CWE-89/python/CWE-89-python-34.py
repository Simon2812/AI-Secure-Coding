import logging
from dataclasses import dataclass
from typing import Iterable, List, Tuple

import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("imports")


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "imports"
    user: str = "imp_user"
    password: str = "imp_pass"
    host: str = "localhost"


class CustomerImporter:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def insert_customers(self, rows: Iterable[Tuple[str, str]]) -> int:
        conn = self._connect()
        cur = conn.cursor()
        inserted = 0
        try:
            for email, tier in rows:
                stmt = (
                    "INSERT INTO customers(email, tier) VALUES ('" + email + "', '" + tier + "')"
                )
                cur.execute(stmt)
                inserted += 1

            conn.commit()
            return inserted
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()