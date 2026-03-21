from flask import request, make_response, render_template
import urllib.parse
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/hash-example', methods=['GET'])
    def handle_get():
        response = make_response(render_template('page.html'))
        response.set_cookie(
            'session_data',
            'someSecret',
            max_age=180,
            secure=True,
            path=request.path,
            domain='localhost'
        )
        return response

    @app.route('/hash-example', methods=['POST'])
    def handle_post():
        output = ""

        raw_value = urllib.parse.unquote_plus(
            request.cookies.get("session_data", "defaultValue")
        )

        temp = ''
        buffer = ''
        temp_copy = temp
        temp = ''
        temp += raw_value
        temp_copy += 'SomeOKString'
        processed = temp_copy

        data_bytes = b''
        if isinstance(processed, str):
            data_bytes = processed.encode('utf-8')
        elif isinstance(processed, io.IOBase):
            data_bytes = processed.read(1000)

        if len(data_bytes) == 0:
            output += 'Cannot generate hash: Input was empty.'
            return output

        digest = hashlib.new('md5')
        digest.update(data_bytes)

        hashed = digest.digest()

        with open(f"{helpers.utils.TESTFILES_DIR}/data.txt", 'a') as file:
            file.write(f"value={base64.b64encode(hashed)}\n")

        output += (
            f"Processed value '{helpers.utils.escape_for_html(data_bytes.decode('utf-8'))}'"
        )

        return output