import psycopg2
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "crm"
    user: str = "crm_user"
    password: str = "crm_pass"
    host: str = "localhost"


class ContactRepository:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def by_emails(self, emails: List[str]) -> List[Tuple]:
        conn = self._connect()
        cur = conn.cursor()

        array_literal = "{" + ",".join(emails) + "}"
        query = (
            "SELECT id, email, full_name "
            "FROM contacts "
            "WHERE email = ANY('" + array_literal + "')"
        )

        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows