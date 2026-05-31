import psycopg2

DB_PASSWORD = "admin123"

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="mydb",
        user="admin",
        password=DB_PASSWORD
    )
    return conn

def fetch_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()
