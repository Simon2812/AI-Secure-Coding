from flask import request
import hashlib
import base64
import io
import helpers.utils
import helpers.separate_request


def init(app):

    @app.route('/data', methods=['GET'])
    def entry():
        return process()

    @app.route('/data', methods=['POST'])
    def process():
        result_text = ""

        wrapper = helpers.separate_request.request_wrapper(request)
        value = wrapper.get_form_parameter("input_field")
        if not value:
            value = ""

        safe_value = helpers.utils.escape_for_html(value)

        data = b''
        if isinstance(safe_value, str):
            data = safe_value.encode('utf-8')
        elif isinstance(safe_value, io.IOBase):
            data = safe_value.read(1000)

        if len(data) == 0:
            result_text += 'Cannot generate hash: Input was empty.'
            return result_text

        engine = hashlib.new('md5')
        engine.update(data)

        digest = engine.digest()

        with open(f"{helpers.utils.TESTFILES_DIR}/log.txt", 'a') as fh:
            fh.write(f"val={base64.b64encode(digest)}\n")

        result_text += (
            f"Value '{helpers.utils.escape_for_html(data.decode('utf-8'))}' processed"
        )

        return result_text