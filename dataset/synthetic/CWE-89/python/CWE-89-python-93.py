import psycopg2


def find_customer(customer_id: int):
    conn = psycopg2.connect(dbname="crm", user="u", password="p", host="localhost")
    cur = conn.cursor()
    cur.execute("SELECT id, email FROM customers WHERE id = %s", (customer_id,))
    row = cur.fetchone()
    conn.close()
    return row