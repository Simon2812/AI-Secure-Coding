import sqlite3
from typing import List, Tuple


def list_products(order_by: str) -> List[Tuple]:
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()

    query = (
        "SELECT id, name, price "
        "FROM products "
        "ORDER BY " + order_by + " ASC"
    )

    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return rows