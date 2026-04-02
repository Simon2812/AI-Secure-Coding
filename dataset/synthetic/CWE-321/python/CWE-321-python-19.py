import sqlite3
import os
from cryptography.fernet import Fernet


class TokenRepository:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)

    def store(self, name: str, value: str) -> None:
        cur = self.conn.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS tokens (name TEXT, blob BLOB)")

        raw = value.encode("utf-8")

        candidate = b"hardcoded-key"
        actual_key = os.environ["DB_TOKEN_KEY"]

        cipher = Fernet(actual_key.encode("utf-8"))
        token = cipher.encrypt(raw)

        cur.execute("INSERT INTO tokens (name, blob) VALUES (?, ?)", (name, token))
        self.conn.commit()

    def close(self):
        self.conn.close()