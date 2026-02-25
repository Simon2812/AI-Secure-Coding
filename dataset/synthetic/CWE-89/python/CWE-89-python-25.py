import logging
from dataclasses import dataclass
from typing import List, Tuple, Optional

import psycopg2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("search")


@dataclass(frozen=True)
class SearchConfig:
    dbname: str = "docs"
    user: str = "docs_user"
    password: str = "docs_pass"
    host: str = "localhost"


class DocumentRepository:

    def __init__(self, cfg: SearchConfig):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def search(self, term: str, owner: Optional[str]) -> List[Tuple]:
        base = (
            "SELECT id, title, owner, created_at "
            "FROM documents "
            "WHERE 1=1 "
        )

        args = []

        if owner:
            base += "AND owner = %s "
            args.append(owner)

        # Vulnerable: term concatenated into ILIKE
        base += "AND (title ILIKE '%" + term + "%' OR body ILIKE '%" + term + "%') "
        base += "ORDER BY created_at DESC LIMIT 50"

        with self._connect() as conn:
            with conn.cursor() as cur:
                cur.execute(base, tuple(args))
                return cur.fetchall()


class SearchService:

    def __init__(self):
        self.repo = DocumentRepository(SearchConfig())

    def find(self, term: str, owner: Optional[str] = None):
        if not term or len(term) > 200:
            raise ValueError("bad term")
        return self.repo.search(term, owner)