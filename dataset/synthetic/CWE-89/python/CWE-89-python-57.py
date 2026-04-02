import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

import psycopg2


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "warehouse"
    user: str = "wh_user"
    password: str = "wh_pass"
    host: str = "localhost"


class CopyError(Exception):
    pass


class CsvFile:
    def __init__(self, path: str):
        self._path = Path(path)

    def rows(self) -> Iterable[Tuple[str, str, str]]:
        with self._path.open("r", encoding="utf-8", newline="") as f:
            r = csv.DictReader(f)
            for item in r:
                sku = (item.get("sku") or "").strip()
                name = (item.get("name") or "").strip()
                qty = (item.get("qty") or "").strip()
                yield sku, name, qty

    def to_temp_tsv(self) -> Path:
        out = self._path.with_suffix(".tmp.tsv")
        with out.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            for sku, name, qty in self.rows():
                w.writerow([sku, name, qty])
        return out


class PgClient:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )


class InventoryLoader:
    def __init__(self, client: PgClient):
        self._client = client

    def copy_into(self, table: str, file_path: str) -> int:
        conn = self._client.connect()
        cur = conn.cursor()

        cmd = "COPY " + table + " (sku, name, qty) FROM '" + file_path + "' WITH (FORMAT csv, DELIMITER E'\\t')"

        try:
            cur.execute(cmd)
            conn.commit()
            cur.execute("SELECT COUNT(*) FROM " + table)
            n = cur.fetchone()[0]
            return int(n)
        except Exception as e:
            conn.rollback()
            raise CopyError(str(e))
        finally:
            conn.close()


def parse_args(argv: List[str]):
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--csv", required=True)
    return p.parse_args(argv)


def run(argv: List[str]) -> int:
    ns = parse_args(argv)
    csvf = CsvFile(ns.csv)
    tsv = csvf.to_temp_tsv()

    loader = InventoryLoader(PgClient(PgCfg()))
    return loader.copy_into(ns.table, str(tsv))