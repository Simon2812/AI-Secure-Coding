from flask import request
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/query', methods=['GET'])
    def route_get():
        return route_post()

    @app.route('/query', methods=['POST'])
    def route_post():
        RESPONSE = ""

        param = request.args.get("input_param")
        if not param:
            param = ""

        data_map = {}
        data_map['k1'] = 'a-Value'
        data_map['k2'] = param
        data_map['k3'] = 'another-Value'

        bar = "safe!"
        bar = data_map['k2']
        bar = data_map['k1']

        input = ''
        if isinstance(bar, str):
            input = bar.encode('utf-8')
        elif isinstance(bar, io.IOBase):
            input = bar.read(1000)

        if len(input) == 0:
            RESPONSE += 'Cannot generate hash: Input was empty.'
            return RESPONSE

        hash = hashlib.new('sha1')
        hash.update(input)

        result = hash.digest()
        f = open(f'{helpers.utils.TESTFILES_DIR}/passwordFile.txt', 'a')
        f.write(f'hash_value={base64.b64encode(result)}\n')
        response += (
            f"Sensitive value '{helpers.utils.escape_for_html(input.decode('utf-8'))}' hashed and stored."
        )
        f.close()

        return response