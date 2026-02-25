from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html


def init(app):

        @app.route('/app/profile', methods=['GET'])
        def profile_get():
                return profile_post()

        @app.route('/app/profile', methods=['POST'])
        def profile_post():
                RESPONSE = ""

                import helpers.separate_request

                wrapped = helpers.separate_request.request_wrapper(request)
                param = wrapped.get_form_parameter("profile")
                if not param:
                        param = ""

                import configparser

                bar = 'safe!'
                conf59255 = configparser.ConfigParser()
                conf59255.add_section('section59255')
                conf59255.set('section59255', 'keyA-59255', 'a_Value')
                conf59255.set('section59255', 'keyB-59255', param)
                bar = conf59255.get('section59255', 'keyA-59255')

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