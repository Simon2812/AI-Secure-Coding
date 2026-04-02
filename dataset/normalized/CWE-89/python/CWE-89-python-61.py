from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html


def init(app):

        @app.route('/app/sqli-00/UserLookup00011', methods=['GET'])
        def UserLookup00011_get():
                response = make_response(render_template('web/sqli-00/UserLookup00011.html'))
                response.set_cookie('UserLookup00011', 'bar',
                        max_age=60*3,
                        secure=True,
                        path=request.path,
                        domain='localhost')
                return response

        @app.route('/app/sqli-00/UserLookup00011', methods=['POST'])
        def UserLookup00011_post():
                RESPONSE = ""

                import urllib.parse
                param = urllib.parse.unquote_plus(request.cookies.get("UserLookup00011", "noCookieValueSupplied"))

                bar = "This should never happen"
                if 'should' in bar:
                        bar = param

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