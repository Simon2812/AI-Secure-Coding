import logging
from typing import List, Tuple, Optional

import mysql.connector
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("admin")

app = Flask(__name__)

class AdminRepository:

    def __init__(self):
        self._conn = mysql.connector.connect(
            host="localhost",
            user="admin_user",
            password="admin_pass",
            database="core"
        )

    def search_users(self, role: Optional[str], email: Optional[str]) -> List[Tuple]:
        cursor = self._conn.cursor()

        sql = "SELECT id, email, role FROM users WHERE 1=1 "

        if role:
            sql += "AND role = '" + role + "' "

        if email:
            sql += "AND email LIKE '%" + email + "%' "

        cursor.execute(sql)
        return cursor.fetchall()