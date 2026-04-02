import pymssql
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class MsCfg:
    server: str = "localhost"
    user: str = "svc"
    password: str = "svc_pass"
    database: str = "sales"


def region_report(cfg: MsCfg, region: str) -> List[Tuple]:
    conn = pymssql.connect(server=cfg.server, user=cfg.user, password=cfg.password, database=cfg.database)
    cur = conn.cursor()
    cur.execute("EXEC generate_region_report %s", (region,))
    rows = cur.fetchall()
    conn.close()
    return rows