from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    conn = sqlite3.connect("auth.db")
    cur = conn.cursor()
    sql = "SELECT id FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    cur.execute(sql)
    row = cur.fetchone()
    return "ok" if row else "fail"
