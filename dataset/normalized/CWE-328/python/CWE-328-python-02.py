from flask import request
import hashlib
import base64
import io
import helpers.utils


def init(app):

    @app.route('/process-input', methods=['GET'])
    def entry_point():
        return handle_request()

    @app.route('/process-input', methods=['POST'])
    def handle_request():
        response_text = ""

        user_value = request.form.get("input_value")
        if not user_value:
            user_value = ""

        condition = "This should never happen"
        if 'should' not in condition:
            selected = "fallback"
        else:
            selected = user_value

        data = b''
        if isinstance(selected, str):
            data = selected.encode('utf-8')
        elif isinstance(selected, io.IOBase):
            data = selected.read(1000)

        if len(data) == 0:
            response_text += 'Cannot generate hash: Input was empty.'
            return response_text

        hasher = hashlib.md5()
        hasher.update(data)

        digest = hasher.digest()

        with open(f"{helpers.utils.TESTFILES_DIR}/records.txt", 'a') as out:
            out.write(f"value={base64.b64encode(digest)}\n")

        response_text += (
            f"Stored value '{helpers.utils.escape_for_html(data.decode('utf-8'))}'"
        )

        return response_text