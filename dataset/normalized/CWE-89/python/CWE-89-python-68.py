from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html


def init(app):

        @app.route('/app/sqli-00/UserLookup01021', methods=['GET'])
        def UserLookup01021_get():
                return UserLookup01021_post()

        @app.route('/app/sqli-00/UserLookup01021', methods=['POST'])
        def UserLookup01021_post():
                RESPONSE = ""

                parts = request.path.split("/")
                param = parts[1]
                if not param:
                        param = ""

                bar = "alsosafe"
                if param:
                        lst = []
                        lst.append('safe')
                        lst.append(param)
                        lst.append('moresafe')
                        lst.pop(0)
                        bar = lst[1]

                import helpers.db_sqlite

                sql = f'SELECT username from USERS where password = ?'
                con = helpers.db_sqlite.get_connection()
                cur = con.cursor()
                cur.execute(sql, (bar,))
                RESPONSE += (
                        helpers.db_sqlite.results(cur, sql)
                )
                con.close()

                return RESPONSE