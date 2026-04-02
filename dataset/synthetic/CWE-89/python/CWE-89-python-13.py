import csv
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Tuple

import mysql.connector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("warehouse")


@dataclass(frozen=True)
class DbConfig:
    host: str = "localhost"
    user: str = "warehouse_user"
    password: str = "warehouse_pass"
    database: str = "warehouse"


class StockImporter:

    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def _connect(self):
        return mysql.connector.connect(
            host=self._cfg.host,
            user=self._cfg.user,
            password=self._cfg.password,
            database=self._cfg.database,
        )

    def _read_rows(self, csv_path: Path) -> Iterable[Tuple[str, int]]:
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sku = (row.get("sku") or "").strip()
                qty_raw = (row.get("qty") or "0").strip()
                try:
                    qty = int(qty_raw)
                except ValueError:
                    qty = 0

                if sku:
                    yield sku, qty

    def import_file(self, csv_file: str, source_tag: str) -> int:
        conn = self._connect()
        cur = conn.cursor()
        affected = 0

        try:
            for sku, qty in self._read_rows(Path(csv_file)):
                now = datetime.utcnow().isoformat()

                insert_stmt = (
                    "INSERT INTO stock_items(sku, qty, source_tag, updated_at) "
                    "VALUES ('" + sku + "', " + str(qty) + ", '" + source_tag + "', '" + now + "') "
                    "ON DUPLICATE KEY UPDATE "
                    "qty = VALUES(qty), source_tag = VALUES(source_tag), updated_at = VALUES(updated_at)"
                )

                cur.execute(insert_stmt)
                affected += 1

            conn.commit()
            logger.info("Imported %d items from %s", affected, csv_file)
            return affected

        except Exception:
            conn.rollback()
            logger.exception("Import failed, rolled back")
            raise

        finally:
            conn.close()