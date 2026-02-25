'''
Example SQL test case

Author: Internal
Created: 2025
'''

from flask import request
from helpers.utils import escape_for_html

def init(app):

    @app.route('/app/testcase-00455', methods=['GET'])
    def testcase_00455_get():
        return testcase_00455_post()

    @app.route('/app/testcase-00455', methods=['POST'])
    def testcase_00455_post():
        RESPONSE = ""

        param = request.headers.get("X-Input-00455")
        if not param:
            param = ""

        data_map = {}
        data_map['keyA'] = 'a-Value'
        data_map['keyB'] = param
        data_map['keyC'] = 'another-Value'
        bar = data_map['keyB']

        import helpers.db_sqlite

        sql = f"SELECT username FROM users WHERE password = '{bar}'"
        con = helpers.db_sqlite.get_connection()
        cur = con.cursor()
        cur.execute(sql)
        RESPONSE += helpers.db_sqlite.results(cur, sql)
        con.close()

        return RESPONSE