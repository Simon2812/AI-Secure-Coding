import sqlite3


def create_user(email: str, role: str):
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, role) VALUES (?, ?)",
        (email, role)
    )
    conn.commit()
    conn.close()