import sqlite3

def load_user(username: str):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()

    query = f"SELECT id, email FROM users WHERE username = '{username}'"
    cur.execute(query)

    row = cur.fetchone()
    conn.close()
    return row