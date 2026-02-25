import argparse
import csv
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import psycopg2
from psycopg2 import sql


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "reporting"
    user: str = "rep_user"
    password: str = "rep_pass"
    host: str = "localhost"


class ExportFailure(Exception):
    pass


class Db:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )


def parse_filters(pairs: Sequence[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            continue
        k, v = item.split("=", 1)
        k = k.strip()
        v = v.strip()
        if k:
            out[k] = v
    return out


class SafeExporter:
    def __init__(self, db: Db):
        self._db = db

    def _build_where(self, filters: Dict[str, str], allowed_cols: List[str]) -> Tuple[sql.SQL, List[object]]:
        clauses: List[sql.SQL] = []
        params: List[object] = []

        for key, val in filters.items():
            if key not in allowed_cols:
                continue
            clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))
            params.append(val)

        if not clauses:
            return sql.SQL(""), params

        return sql.SQL(" WHERE ") + sql.SQL(" AND ").join(clauses), params

    def export(
        self,
        table: str,
        columns: List[str],
        filters: Dict[str, str],
        out_path: str,
        limit: int
    ) -> int:
        if not columns:
            raise ExportFailure("no columns")

        allowed_cols = list(columns)

        where_sql, params = self._build_where(filters, allowed_cols)

        stmt = (
            sql.SQL("SELECT ")
            + sql.SQL(", ").join(sql.Identifier(c) for c in columns)
            + sql.SQL(" FROM ")
            + sql.Identifier(table)
            + where_sql
            + sql.SQL(" ORDER BY ")
            + sql.Identifier(columns[0])
            + sql.SQL(" LIMIT %s")
        )

        params.append(int(limit))

        conn = self._db.connect()
        cur = conn.cursor()
        try:
            cur.execute(stmt, params)
            rows = cur.fetchall()
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(columns)
                for r in rows:
                    w.writerow(list(r))
            return len(rows)
        except Exception as e:
            raise ExportFailure(str(e))
        finally:
            conn.close()


def parse_args(argv: List[str]):
    p = argparse.ArgumentParser()
    p.add_argument("--table", required=True)
    p.add_argument("--col", action="append", default=[])
    p.add_argument("--where", action="append", default=[])
    p.add_argument("--out", required=True)
    p.add_argument("--limit", default="100")
    return p.parse_args(argv)


def run(argv: List[str]) -> int:
    ns = parse_args(argv)
    filters = parse_filters(ns.where)
    exporter = SafeExporter(Db(PgCfg()))
    return exporter.export(
        table=ns.table,
        columns=list(ns.col),
        filters=filters,
        out_path=ns.out,
        limit=int(ns.limit)
    )