import mysql.connector

_ALLOWED_FIELDS = {"created_at", "priority", "status", "id"}

def list_tickets(sort_field: str):
    db = mysql.connector.connect(
        host="localhost",
        user="helpdesk_user",
        password="helpdesk_pass",
        database="helpdesk"
    )
    cur = db.cursor()

    clause = "ORDER BY " + sort_field + " DESC"
    command = "SELECT id, subject, status FROM tickets " + clause
    cur.execute(command)
    rows = cur.fetchall()

    db.close()
    return rows