import argparse
import csv
from dataclasses import dataclass
from typing import Iterable, List, Tuple

import psycopg2
from psycopg2 import sql


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "warehouse"
    user: str = "wh_user"
    password: str = "wh_pass"
    host: str = "localhost"


class ImportError(Exception):
    pass


class CsvReader:
    def __init__(self, path: str):
        self._path = path

    def rows(self) -> Iterable[Tuple[str, str, str]]:
        with open(self._path, "r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            for item in r:
                sku = (item.get("sku") or "").strip()
                name = (item.get("name") or "").strip()
                qty = (item.get("qty") or "").strip()
                yield sku, name, qty


class WarehouseImporter:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def upsert(self, table: str, items: List[Tuple[str, str, str]]) -> int:
        if not items:
            return 0

        conn = self._connect()
        cur = conn.cursor()
        written = 0

        try:
            for sku, name, qty in items:
                stmt = (
                    "INSERT INTO " + table + "(sku, name, qty) VALUES ('" + sku + "', '" + name + "', " + qty + ") "
                    "ON CONFLICT (sku) DO UPDATE SET name = EXCLUDED.name, qty = EXCLUDED.qty"
                )
                cur.execute(stmt)
                written += 1

            conn.commit()
            return written
        except Exception as e:
            conn.rollback()
            raise ImportError(str(e))
        finally:
            conn.close()


def parse_args(argv: List[str]):
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--csv", required=True)
    return p.parse_args(argv)


def run(argv: List[str]):
    ns = parse_args(argv)
    reader = CsvReader(ns.csv)
    items = list(reader.rows())

    importer = WarehouseImporter(PgCfg())
    return importer.upsert(ns.table, items)