import sqlite3
from typing import List, Tuple


def users_with_flag(flag: str) -> List[Tuple]:
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    query = (
        "SELECT u.id, u.email "
        "FROM users u "
        "WHERE EXISTS("
        "  SELECT 1 FROM user_flags f "
        "  WHERE f.user_id = u.id AND f.flag = '" + flag + "'"
        ")"
    )

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows