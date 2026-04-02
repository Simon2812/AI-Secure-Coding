from django.db import connection
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class FeedParams:
    category: Optional[str]
    page_size: int
    offset: str


class FeedRepository:
    def load(self, params: FeedParams) -> List[Tuple]:
        sql = (
            "SELECT id, title, category, created_at "
            "FROM posts "
            "WHERE 1=1 "
        )
        values = []

        if params.category:
            sql += "AND category = %s "
            values.append(params.category)

        sql += "ORDER BY created_at DESC LIMIT %s OFFSET " + params.offset
        values.append(params.page_size)

        with connection.cursor() as cur:
            cur.execute(sql, values)
            return cur.fetchall()