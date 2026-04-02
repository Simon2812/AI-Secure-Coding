import psycopg2
from typing import List, Tuple


def top_users(limit: int) -> List[Tuple]:
    conn = psycopg2.connect(dbname="stats", user="u", password="p", host="localhost")
    cur = conn.cursor()

    query = (
        "SELECT user_id, SUM(score) AS total, "
        "RANK() OVER (ORDER BY SUM(score) DESC) AS rnk "
        "FROM game_scores "
        "GROUP BY user_id "
        "ORDER BY total DESC LIMIT %s"
    )

    cur.execute(query, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows