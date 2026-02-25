from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

    @app.route('/home/sql/something', methods=['GET'])
    def something_get():
        return BenchmarkTest00099_post()

    @app.route('/home/sql/something', methods=['POST'])
    def something_post():
        RESPONSE = ""

        param = request.form.get("something")
        if not param:
            param = ""

        import configparser
        
        bar = 'safe!'
        conf52528 = configparser.ConfigParser()
        conf52528.add_section('section52528')
        conf52528.set('section52528', 'keyA-52528', 'a-Value')
        conf52528.set('section52528', 'keyB-52528', param)
        bar = conf52528.get('section52528', 'keyB-52528')

        import helpers.db_sqlite

        sql = f'SELECT username from USERS where password = \'{bar}\''
        con = helpers.db_sqlite.get_connection()
        cur = con.cursor()
        cur.execute(sql)
        RESPONSE += (
            helpers.db_sqlite.results(cur, sql)
        )
        con.close()

        return RESPONSE
