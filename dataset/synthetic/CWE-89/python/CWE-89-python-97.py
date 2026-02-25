import psycopg2


def update_email(user_id: int, email: str):
    conn = psycopg2.connect(dbname="crm", user="u", password="p", host="localhost")
    try:
        cur = conn.cursor()
        cur.execute("UPDATE users SET email = %s WHERE id = %s", (email, user_id))
        conn.commit()
    finally:
        conn.close()