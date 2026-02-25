import sqlite3

def has_orders(email: str):
    conn = sqlite3.connect("shop.db")
    cur = conn.cursor()

    query = (
        "SELECT EXISTS("
        "SELECT 1 FROM orders WHERE customer_email = '" + email + "'"
        ")"
    )

    cur.execute(query)
    result = cur.fetchone()
    conn.close()
    return bool(result and result[0])