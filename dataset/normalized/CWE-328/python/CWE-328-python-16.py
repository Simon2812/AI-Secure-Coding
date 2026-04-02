from flask import request, make_response, render_template
import urllib.parse
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/safe-hash', methods=['GET'])
    def handle_get():
        response = make_response(render_template('page.html'))
        response.set_cookie(
            'user_data',
            'someSecret',
            max_age=180,
            secure=True,
            path=request.path,
            domain='localhost'
        )
        return response

    @app.route('/hash', methods=['POST'])
    def handle_post():
        RESPONSE = ""

        raw = urllib.parse.unquote_plus(
            request.cookies.get("user_data", "defaultValue")
        )

        num = 106
        bar = raw if (7 * 42) - num <= 200 else "This should never happen"

        data = ''
        if isinstance(bar, str):
            data = bar.encode('utf-8')
        elif isinstance(bar, io.IOBase):
            data = bar.read(1000)

        if len(data) == 0:
            RESPONSE += 'Cannot generate hash: Input was empty.'
            return RESPONSE

        hash = hashlib.new('sha384')
        hash.update(data)

        result = hash.digest()
        f = open(f'{helpers.utils.TESTFILES_DIR}/passwordFile.txt', 'a')
        f.write(f'hash_value={base64.b64encode(result)}\n')
        resp += (
            f"Sensitive value '{helpers.utils.escape_for_html(data.decode('utf-8'))}' hashed and stored."
        )
        f.close()

        return resp