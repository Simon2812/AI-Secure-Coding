import pymysql

def is_admin(user_id: str):
    conn = pymysql.connect(host="localhost", user="app", password="pass", database="appdb")
    cur = conn.cursor()

    sql = "SELECT is_admin FROM users WHERE id = " + user_id
    cur.execute(sql)

    row = cur.fetchone()
    conn.close()
    return bool(row and row[0])