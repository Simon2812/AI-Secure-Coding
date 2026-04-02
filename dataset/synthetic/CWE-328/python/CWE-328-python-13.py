from flask import request
import hashlib
import helpers.utils


def compute_hash(data):
    return hashlib.md5(data).digest()


def init(app):

    @app.route('/process-data', methods=['POST'])
    def process_data():
        response = ""

        value = request.form.get("input")
        if not value:
            value = ""

        payload = value.encode('utf-8')

        if len(payload) == 0:
            return 'empty'

        result = compute_hash(payload)

        response += f"{helpers.utils.escape_for_html(str(result))}"
        return response