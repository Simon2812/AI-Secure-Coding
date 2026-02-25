import sqlite3

def load_account(account_name):
    connection = sqlite3.connect("accounts.db")
    db_cursor = connection.cursor()

    stmt = f"SELECT id, balance FROM accounts WHERE name = '{account_name}'"
    records = db_cursor.execute(stmt).fetchall()

    connection.close()
    return records