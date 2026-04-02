import logging
import sqlite3
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sessions")

app = Flask(__name__)


def open_db() -> sqlite3.Connection:
    return sqlite3.connect("app.db")


class SessionRepository:
    def delete_for_user(self, username: str) -> int:
        conn = open_db()
        cur = conn.cursor()

        script = (
            "DELETE FROM sessions "
            "WHERE username = '" + username + "';"
        )

        cur.executescript(script)
        conn.commit()
        affected = cur.rowcount
        conn.close()
        return affected


repo = SessionRepository()


@app.post("/sessions/purge")
def purge():
    username = request.json.get("username", "")
    removed = repo.delete_for_user(username)
    return jsonify({"removed": removed})