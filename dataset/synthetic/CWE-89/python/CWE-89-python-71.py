import sqlite3
import pandas as pd


def load_sessions(user_id: int):
    conn = sqlite3.connect("analytics.db")
    query = "SELECT id, started_at FROM sessions WHERE user_id = ? ORDER BY started_at DESC"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df