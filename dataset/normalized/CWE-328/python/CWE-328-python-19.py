from flask import request
import hashlib
import base64
import io
import helpers.utils
import helpers.separate_request


def init(app):

    @app.route('/wrapped-input', methods=['GET'])
    def route_get():
        return route_post()

    @app.route('/wrapped-input', methods=['POST'])
    def route_post():
        RESPONSE = ""

        wrapper = helpers.separate_request.request_wrapper(request)
        value = wrapper.get_form_parameter("input_name")
        if not value:
            value = ""

        bar = value

        data = ''
        if isinstance(bar, str):
            data = bar.encode('utf-8')
        elif isinstance(bar, io.IOBase):
            data = bar.read(1000)

        if len(data) == 0:
            RESPONSE += 'Cannot generate hash: Input was empty.'
            return RESPONSE

        hash = hashlib.new('sha512')
        hash.update(data)

        result = hash.digest()
        f = open(f'{helpers.utils.TESTFILES_DIR}/passwordFile.txt', 'a')
        f.write(f'hash_value={base64.b64encode(result)}\n')
        RESPONSE += (
            f"Sensitive value '{helpers.utils.escape_for_html(data.decode('utf-8'))}' hashed and stored."
        )
        f.close()

        return RESPONSE