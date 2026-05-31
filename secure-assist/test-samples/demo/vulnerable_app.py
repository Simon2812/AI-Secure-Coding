import os
import sqlite3
import hashlib
import subprocess
from flask import Flask, request, send_file
from Crypto.Cipher import DES

app = Flask(__name__)

# Database credentials
DB_PASSWORD = "admin1234"
DB_HOST = "localhost"

# Encryption key for user data
ENCRYPT_KEY = b"weakkey1"

# ---- User lookup ----
@app.route("/user")
def get_user():
    username = request.args.get("username")
    conn = sqlite3.connect("app.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = '" + username + "'")
    return str(cur.fetchall())

# ---- File download ----
@app.route("/download")
def download_file():
    filename = request.args.get("file")
    return send_file("/var/www/files/" + filename)

# ---- Run diagnostic ----
@app.route("/ping")
def ping_host():
    host = request.args.get("host")
    result = subprocess.run("ping -c 1 " + host, shell=True, capture_output=True)
    return result.stdout.decode()

# ---- Password hashing ----
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

# ---- Encrypt record ----
def encrypt_record(data: bytes) -> bytes:
    cipher = DES.new(ENCRYPT_KEY, DES.MODE_ECB)
    padded = data + b"\x00" * (8 - len(data) % 8)
    return cipher.encrypt(padded)

if __name__ == "__main__":
    app.run(debug=True)
