from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

    @app.route('/app/testcase-00454', methods=['GET'])
    def case_00454_get():
        return testcase_00454_post()

    @app.route('/app/testcase-00454', methods=['POST'])
    def case_00454_post():
        RESPONSE = ""

        param = request.headers.get("X-Custom-Input")
        if not param:
            param = ""

        import base64
        tmp = base64.b64encode(param.encode('utf-8'))
        bar = base64.b64decode(tmp).decode('utf-8')

        import helpers.db_sqlite

        sql = f"SELECT username FROM users WHERE password = '{bar}'"
        con = helpers.db_sqlite.get_connection()
        cur = con.cursor()
        cur.execute(sql)
        RESPONSE += (
            helpers.db_sqlite.results(cur, sql)
        )
        con.close()

        return RESPONSE