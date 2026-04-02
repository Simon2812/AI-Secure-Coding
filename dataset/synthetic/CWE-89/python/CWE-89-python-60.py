import argparse
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import psycopg2
from psycopg2 import sql


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "accounts"
    user: str = "acct_user"
    password: str = "acct_pass"
    host: str = "localhost"


class UpdateError(Exception):
    pass


class AccountUpdater:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def update(self, table: str, account_id: str, fields: Dict[str, str]) -> Optional[Tuple]:
        if not fields:
            return None

        conn = self._connect()
        cur = conn.cursor()

        assignments = ", ".join(f"{k} = '{v}'" for k, v in fields.items())
        query = "UPDATE " + table + " SET " + assignments + " WHERE id = " + account_id + " RETURNING id, email"

        try:
            cur.execute(query)
            row = cur.fetchone()
            conn.commit()
            return row
        except Exception as e:
            conn.rollback()
            raise UpdateError(str(e))
        finally:
            conn.close()


def parse_kv(pairs: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            continue
        k, v = item.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def parse_args(argv: List[str]):
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--set", action="append", default=[])
    return p.parse_args(argv)


def run(argv: List[str]):
    ns = parse_args(argv)
    fields = parse_kv(ns.set)
    updater = AccountUpdater(PgCfg())
    return updater.update(ns.table, ns.id, fields)