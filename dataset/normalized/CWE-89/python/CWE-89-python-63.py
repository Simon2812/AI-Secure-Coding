from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html


def init(app):

        @app.route('/app/sqli-00/UserLookup00100', methods=['GET'])
        def UserLookup00100_get():
                return UserLookup00100_post()

        @app.route('/app/sqli-00/UserLookup00100', methods=['POST'])
        def UserLookup00100_post():
                RESPONSE = ""

                param = request.form.get("UserLookup00100")
                if not param:
                        param = ""

                map87 = {}
                map87['keyA-87'] = 'a-Value'
                map87['keyB-87'] = param
                map87['keyC'] = 'another-Value'
                bar = "safe!"
                bar = map87['keyB-87']
                bar = map87['keyA-87']

                import helpers.db_sqlite

                sql = f'SELECT username from USERS where password = ?'
                con = helpers.db_sqlite.get_connection()
                cur = con.cursor()
                cur.execute(sql, (bar,))
                RESPONSE += (
                        helpers.db_sqlite.results(cur, sql)
                )
                con.close()

                return RESPONSEs