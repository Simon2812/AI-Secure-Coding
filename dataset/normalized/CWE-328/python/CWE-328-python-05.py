from flask import request
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/header', methods=['GET'])
    def get_handler():
        return post_handler()

    @app.route('/header', methods=['POST'])
    def post_handler():
        RESPONSE = ""

        param = request.headers.get("input_header")
        if not param:
            param = ""

        tmp = ''
        data = ''
        copy = tmp
        tmp = ''
        tmp += param
        copy += 'SomeOKString'
        bar = copy

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

        out = hash.digest()
        f = open(f'{helpers.utils.TESTFILES_DIR}/passwordFile.txt', 'a')
        f.write(f'hash_value={base64.b64encode(out)}\n')
        resp += (
            f"Sensitive value '{helpers.utils.escape_for_html(input.decode('utf-8'))}' hashed and stored."
        )
        f.close()

        return resp