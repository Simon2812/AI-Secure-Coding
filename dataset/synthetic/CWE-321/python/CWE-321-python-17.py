import os
import sqlite3
import json
from typing import Dict, Any
from cryptography.fernet import Fernet


class AuditStore:
    def __init__(self, db_path: str):
        self._conn = sqlite3.connect(db_path)

    def insert_record(self, record: Dict[str, Any]) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS audit (id TEXT, blob BLOB)"
        )

        payload = json.dumps(record).encode("utf-8")

        key_material = os.getenv("AUDIT_KEY").encode("utf-8")
        cipher = Fernet(key_material)

        encrypted = cipher.encrypt(payload)

        cursor.execute(
            "INSERT INTO audit (id, blob) VALUES (?, ?)",
            (record.get("id"), encrypted)
        )

        self._conn.commit()

    def close(self):
        self._conn.close()