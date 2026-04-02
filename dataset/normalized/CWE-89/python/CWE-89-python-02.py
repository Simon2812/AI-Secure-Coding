from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

    @app.route('/site/sql-00/important', methods=['GET'])
    def my_get():
        return BenchmarkTest00283_post()

    @app.route('/site/sql-00/important', methods=['POST'])
    def my_post():
        RESPONSE = ""

        import helpers.separate_request
        
        wrapped = helpers.separate_request.request_wrapper(request)
        param = wrapped.get_form_parameter("important")
        if not param:
            param = ""

        map8812 = {}
        map8812['keyA-8812'] = 'a-Value'
        map8812['keyB-8812'] = param
        map8812['keyC'] = 'another-Value'
        bar = map8812['keyB-8812']

        import helpers.db_sqlite

        query = f'SELECT username from USERS where password = \'{bar}\''
        con = helpers.db_sqlite.get_connection()
        cur = con.cursor()
        cur.execute(query)
        RESPONSE += (
            helpers.db_sqlite.results(cur, query)
        )
        con.close()

        return RESPONSE