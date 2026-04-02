from flask import request
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/headers-check', methods=['GET'])
    def route_get():
        return route_post()

    @app.route('/headers-check', methods=['POST'])
    def route_post():
        RESPONSE = ""

        param = ""

        for name in request.headers.keys():
            if name.lower() in helpers.utils.commonHeaderNames:
                continue

            if request.headers.get_all(name):
                param = name
                break

        bar = param

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