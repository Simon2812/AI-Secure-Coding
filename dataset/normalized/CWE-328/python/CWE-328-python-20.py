from flask import request
import html
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/header-process', methods=['GET'])
    def handle_get():
        return handle_post()

    @app.route('/header-process', methods=['POST'])
    def handle_post():
        RESPONSE = ""

        value = request.headers.get("input_header")
        if not value:
            value = ""

        bar = html.escape(value)

        data = ''
        if isinstance(bar, str):
            data = bar.encode('utf-8')
        elif isinstance(bar, io.IOBase):
            data = bar.read(1000)

        if len(data) == 0:
            RESPONSE += 'Cannot generate hash: Input was empty.'
            return RESPONSE

        hash = hashlib.new('sha256')
        hash.update(data)

        out = hash.digest()
        f = open(f'{helpers.utils.TESTFILES_DIR}/passwordFile.txt', 'a')
        f.write(f'hash_value={base64.b64encode(out)}\n')
        resp += (
            f"Sensitive value '{helpers.utils.escape_for_html(data.decode('utf-8'))}' hashed and stored."
        )
        f.close()

        return resp
