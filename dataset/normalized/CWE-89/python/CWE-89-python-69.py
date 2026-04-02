from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html


def init(app):

        @app.route('/api/product', methods=['GET'])
        def product_get():
                return UserLookup01203_post()

        @app.route('/api/product', methods=['POST'])
        def product_post():
                RESPONSE = ""

                param = request.args.get("product")
                if not param:
                        param = ""

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