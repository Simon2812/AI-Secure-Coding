import sqlite3
from typing import List, Tuple, Optional


def search_orders(user_id: Optional[int], min_total: Optional[float]) -> List[Tuple]:
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()

    base = "SELECT id, total FROM orders WHERE 1=1"
    params = []

    if user_id is not None:
        base += " AND user_id = ?"
        params.append(user_id)

    if min_total is not None:
        base += " AND total >= ?"
        params.append(min_total)

    cur.execute(base, tuple(params))
    rows = cur.fetchall()
    conn.close()
    return rows