import argparse
import csv
from dataclasses import dataclass
from typing import Iterable, List, Tuple
import psycopg2


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "inventory"
    user: str = "inv"
    password: str = "invpass"
    host: str = "localhost"


class Importer:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def read_rows(self, path: str) -> Iterable[Tuple[str, int]]:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row["sku"], int(row["qty"])

    def upsert(self, rows: Iterable[Tuple[str, int]]):
        conn = self._connect()
        cur = conn.cursor()
        stmt = (
            "INSERT INTO stock (sku, qty) VALUES (%s, %s) "
            "ON CONFLICT (sku) DO UPDATE SET qty = EXCLUDED.qty"
        )
        try:
            for sku, qty in rows:
                cur.execute(stmt, (sku, qty))
            conn.commit()
        finally:
            conn.close()


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    return p.parse_args()


def main():
    args = parse_args()
    importer = Importer(PgCfg())
    rows = importer.read_rows(args.file)
    importer.upsert(rows)


if __name__ == "__main__":
    main()