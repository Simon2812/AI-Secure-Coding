from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html


def init(app):

        @app.route('/api/reports', methods=['GET'])
        def reports_get():
                return UserLookup01229_post()

        @app.route('/api/reports', methods=['POST'])
        def reports_post():
                RESPONSE = ""

                import helpers.separate_request
                scr = helpers.separate_request.request_wrapper(request)
                param = scr.get_safe_value("reports")

                import helpers.db_sqlite

                sql = f'SELECT username from USERS where password = ?'
                con = helpers.db_sqlite.get_connection()
                cur = con.cursor()
                cur.execute(sql, (param,))
                RESPONSE += (
                        helpers.db_sqlite.results(cur, sql)
                )
                con.close()

                return RESPONSE