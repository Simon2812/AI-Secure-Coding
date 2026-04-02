import mysql.connector


def get_account(account_id: int):
    conn = mysql.connector.connect(host="localhost", user="u", password="p", database="bank")
    cur = conn.cursor()
    cur.execute("SELECT id, balance FROM accounts WHERE id = %s", (account_id,))
    row = cur.fetchone()
    conn.close()
    return row