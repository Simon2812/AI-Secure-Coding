from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html


def init(app):

        @app.route('/app/sqli-00/UserLookup', methods=['GET'])
        def UserLookup_get():
                return UserLookup_post()

        @app.route('/app/sqli-00/UserLookup', methods=['POST'])
        def UserLookup_post():
                RESPONSE = ""

                import helpers.separate_request

                wrapped = helpers.separate_request.request_wrapper(request)
                param = wrapped.get_form_parameter("UserLookup")
                if not param:
                        param = ""

                possible = "ABC"
                guess = possible[0]

                match guess:
                        case 'A':
                                bar = param
                        case 'B':
                                bar = 'bob'
                        case 'C' | 'D':
                                bar = param
                        case _:
                                bar = 'bob\'s your uncle'

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