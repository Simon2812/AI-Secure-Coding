from flask import request
from helpers.utils import escape_for_html

def init(app):

    @app.route('/app/testcase-00284', methods=['GET'])
    def testcase_00284_get():
        return testcase_00284_post()

    @app.route('/app/testcase-00284', methods=['POST'])
    def testcase_00284_post():
        RESPONSE = ""

        import helpers.separate_request
        
        wrapped = helpers.separate_request.request_wrapper(request)
        param = wrapped.get_form_parameter("input_00284")
        if not param:
            param = ""

        bar = "This should never happen"
        if 'should' in bar:
            bar = param

        import helpers.db_sqlite

        sql = f"SELECT username FROM users WHERE password = '{bar}'"
        con = helpers.db_sqlite.get_connection()
        cur = con.cursor()
        cur.execute(sql)
        RESPONSE += helpers.db_sqlite.results(cur, sql)
        con.close()

        return RESPONSE