from flask import request
import base64
import hashlib
import io
import helpers.utils


def init(app):

    @app.route('/submit-data', methods=['GET'])
    def route_get():
        return route_post()

    @app.route('/submit-data', methods=['POST'])
    def route_post():
        response_body = ""

        items = request.form.getlist("data")
        value = ""
        if items:
            value = items[0]

        encoded = base64.b64encode(value.encode('utf-8'))
        decoded = base64.b64decode(encoded).decode('utf-8')

        payload = b''
        if isinstance(decoded, str):
            payload = decoded.encode('utf-8')
        elif isinstance(decoded, io.IOBase):
            payload = decoded.read(1000)

        if len(payload) == 0:
            response_body += 'Cannot generate hash: Input was empty.'
            return response_body

        algorithm = hashlib.new('sha1')
        algorithm.update(payload)

        result_bytes = algorithm.digest()

        with open(f"{helpers.utils.TESTFILES_DIR}/output.txt", 'a') as handle:
            handle.write(f"entry={base64.b64encode(result_bytes)}\n")

        response_body += (
            f"Handled value '{helpers.utils.escape_for_html(payload.decode('utf-8'))}'"
        )

        return response_body