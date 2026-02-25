import psycopg2
from typing import List, Tuple


def fetch_by_ids(ids: List[int]) -> List[Tuple]:
    conn = psycopg2.connect(dbname="core", user="u", password="p", host="localhost")
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users WHERE id = ANY(%s)", (ids,))
    rows = cur.fetchall()
    conn.close()
    return rows