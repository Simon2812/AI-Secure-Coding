import csv
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

from django.core.management.base import BaseCommand
from django.db import connection


@dataclass(frozen=True)
class ExportOptions:
    since: str
    region: Optional[str]
    min_amount: Optional[str]
    out_path: str


class ExportError(Exception):
    pass


class PaymentExporter:
    def build_query(self, opts: ExportOptions) -> Tuple[str, List[object]]:
        sql = (
            "SELECT p.id, p.user_id, p.region, p.amount, p.created_at "
            "FROM payments p "
            "WHERE p.created_at >= %s "
        )
        params: List[object] = [opts.since]

        if opts.region:
            sql += "AND p.region = %s "
            params.append(opts.region)

        if opts.min_amount:
            sql += "AND p.amount >= {min_amount} ".format(min_amount=opts.min_amount)

        sql += "ORDER BY p.created_at DESC"
        return sql, params

    def fetch_rows(self, opts: ExportOptions) -> Iterable[Tuple]:
        sql, params = self.build_query(opts)
        with connection.cursor() as cur:
            cur.execute(sql, params)
            for row in cur.fetchall():
                yield row

    def write_csv(self, rows: Iterable[Tuple], out_path: str) -> int:
        count = 0
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "user_id", "region", "amount", "created_at"])
            for r in rows:
                writer.writerow(list(r))
                count += 1
        return count

    def export(self, opts: ExportOptions) -> int:
        rows = self.fetch_rows(opts)
        return self.write_csv(rows, opts.out_path)


def parse_args(**kwargs) -> ExportOptions:
    since = kwargs.get("since")
    out_path = kwargs.get("out")
    region = kwargs.get("region")
    min_amount = kwargs.get("min_amount")

    if not since:
        raise ExportError("missing since")
    if not out_path:
        raise ExportError("missing out")

    return ExportOptions(since=since, region=region, min_amount=min_amount, out_path=out_path)


class Command(BaseCommand):
    help = "Export payments to CSV"

    def add_arguments(self, parser):
        parser.add_argument("--since", required=True)
        parser.add_argument("--out", required=True)
        parser.add_argument("--region", required=False)
        parser.add_argument("--min-amount", required=False)

    def handle(self, *args, **options):
        try:
            opts = parse_args(
                since=options.get("since"),
                out=options.get("out"),
                region=options.get("region"),
                min_amount=options.get("min_amount")
            )
        except ExportError as e:
            raise e

        exporter = PaymentExporter()
        written = exporter.export(opts)
        self.stdout.write(str(written))