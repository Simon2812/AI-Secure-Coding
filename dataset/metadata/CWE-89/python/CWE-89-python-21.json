import logging
from dataclasses import dataclass
from typing import List, Tuple, Optional

from django.db import connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("accounts")

@dataclass(frozen=True)
class SearchFilters:
    email: Optional[str] = None
    country: Optional[str] = None
    only_active: bool = True

class AccountRepository:

    def fetch_accounts(self, filters: SearchFilters, limit: int) -> List[Tuple]:
        statement = (
            "SELECT id, email, country, is_active, created_at "
            "FROM accounts "
            "WHERE 1=1 "
        )

        params = []

        if filters.only_active:
            statement += "AND is_active = 1 "

        if filters.country:
            statement += "AND country = %s "
            params.append(filters.country)

        if filters.email:
            statement += "AND email LIKE '%" + filters.email + "%' "

        statement += "ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        with connection.cursor() as cursor:
            cursor.execute(statement, params)
            return cursor.fetchall()