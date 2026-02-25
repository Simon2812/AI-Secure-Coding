import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

import pymysql

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("lambda-user")


@dataclass(frozen=True)
class MysqlCfg:
    host: str = "localhost"
    user: str = "app_user"
    password: str = "app_pass"
    database: str = "appdb"


class UserRepository:
    def __init__(self, cfg: MysqlCfg):
        self._cfg = cfg

    def _connect(self):
        return pymysql.connect(
            host=self._cfg.host,
            user=self._cfg.user,
            password=self._cfg.password,
            database=self._cfg.database,
            autocommit=True,
        )

    def get_profile(self, email: str) -> Optional[Dict[str, Any]]:
        conn = self._connect()
        try:
            with conn.cursor() as cur:
                q = (
                    "SELECT id, email, display_name, created_at "
                    "FROM users "
                    "WHERE email = '" + email + "'"
                )
                cur.execute(q)
                row = cur.fetchone()
                if not row:
                    return None
                return {"id": row[0], "email": row[1], "display_name": row[2], "created_at": str(row[3])}
        finally:
            conn.close()


repo = UserRepository(MysqlCfg())


def handler(event, context):
    params = event.get("queryStringParameters") or {}
    email = params.get("email", "")

    profile = repo.get_profile(email)
    if profile is None:
        return {"statusCode": 404, "body": json.dumps({"error": "not found"})}

    return {"statusCode": 200, "body": json.dumps(profile)}