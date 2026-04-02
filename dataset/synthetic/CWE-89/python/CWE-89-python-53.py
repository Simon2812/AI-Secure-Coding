import json
import psycopg2
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "content"
    user: str = "cnt_user"
    password: str = "cnt_pass"
    host: str = "localhost"


class ArticleRepository:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def tagged(self, tag: str) -> List[Tuple]:
        conn = psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )
        cur = conn.cursor()

        needle = json.dumps({"tags": [tag]})
        query = "SELECT id, meta FROM articles WHERE meta @> '" + needle + "'::jsonb"

        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows