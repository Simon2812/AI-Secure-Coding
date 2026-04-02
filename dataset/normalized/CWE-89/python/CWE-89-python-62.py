from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html


def init(app):

        @app.route('/app/sqli-00/UserLookup00012', methods=['GET'])
        def UserLookup00012_get():
                response = make_response(render_template('web/sqli-00/UserLookup00012.html'))
                response.set_cookie('UserLookup00012', 'bar',
                        max_age=60*3,
                        secure=True,
                        path=request.path,
                        domain='localhost')
                return response
                return UserLookup00012_post()

        @app.route('/app/sqli-00/UserLookup00012', methods=['POST'])
        def UserLookup00012_post():
                RESPONSE = ""

                import urllib.parse
                param = urllib.parse.unquote_plus(request.cookies.get("UserLookup00012", "noCookieValueSupplied"))

                string93844 = 'help'
                string93844 += param
                string93844 += 'snapes on a plane'
                bar = string93844[4:-17]

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