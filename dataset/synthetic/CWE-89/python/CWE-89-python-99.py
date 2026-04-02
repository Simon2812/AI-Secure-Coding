from flask import Flask, request, jsonify
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import psycopg2


@dataclass(frozen=True)
class PgCfg:
    dbname: str = "app"
    user: str = "u"
    password: str = "p"
    host: str = "localhost"


class UserRepository:
    def __init__(self, cfg: PgCfg):
        self._cfg = cfg

    def _connect(self):
        return psycopg2.connect(
            dbname=self._cfg.dbname,
            user=self._cfg.user,
            password=self._cfg.password,
            host=self._cfg.host
        )

    def list_users(self, role: Optional[str], limit: int) -> List[Dict[str, Any]]:
        conn = self._connect()
        cur = conn.cursor()

        query = "SELECT id, email, role FROM users WHERE 1=1"
        params = []

        if role:
            query += " AND role = %s"
            params.append(role)

        query += " ORDER BY id LIMIT %s"
        params.append(limit)

        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        conn.close()

        return [{"id": r[0], "email": r[1], "role": r[2]} for r in rows]


app = Flask(__name__)
repo = UserRepository(PgCfg())


@app.route("/users")
def users():
    role = request.args.get("role")
    limit = int(request.args.get("limit", "50"))
    return jsonify(repo.list_users(role, limit))


if __name__ == "__main__":
    app.run()