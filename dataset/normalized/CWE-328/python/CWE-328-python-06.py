from flask import request
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/headers', methods=['GET'])
    def get_route():
        return post_route()

    @app.route('/headers', methods=['POST'])
    def post_route():
        RESPONSE = ""

        param = ""
        headers = request.headers.getlist("input_header")

        if headers:
            param = headers[0]

        bar = ''
        if param:
            bar = param.split(' ')[0]

        input = ''
        if isinstance(bar, str):
            input = bar.encode('utf-8')
        elif isinstance(bar, io.IOBase):
            input = bar.read(1000)

        if len(input) == 0:
            RESPONSE += 'Cannot generate hash: Input was empty.'
            return RESPONSE

        hash = hashlib.new('md5')
        hash.update(input)

        result = hash.digest()
        f = open(f'{helpers.utils.TESTFILES_DIR}/passwordFile.txt', 'a')
        f.write(f'hash_value={base64.b64encode(result)}\n')
        RESPONSE += (
            f"Sensitive value '{helpers.utils.escape_for_html(input.decode('utf-8'))}' hashed and stored."
        )
        f.close()

        return RESPONSE