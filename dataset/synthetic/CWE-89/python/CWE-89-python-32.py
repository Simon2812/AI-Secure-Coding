import logging
from dataclasses import dataclass
from typing import List, Tuple

import pyodbc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hr")


@dataclass(frozen=True)
class SqlServerCfg:
    conn_str: str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost;DATABASE=hrdb;UID=hr_user;PWD=hr_pass"
    )


class EmployeeDirectory:
    def __init__(self, cfg: SqlServerCfg):
        self._cfg = cfg

    def find_by_title(self, title: str) -> List[Tuple]:
        conn = pyodbc.connect(self._cfg.conn_str)
        cur = conn.cursor()

        query = (
            "SELECT emp_id, full_name, title "
            "FROM employees "
            "WHERE title = '" + title + "'"
        )

        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return rows