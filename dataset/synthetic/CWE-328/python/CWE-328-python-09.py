from flask import request
import hashlib
import helpers.utils


def init(app):

    @app.route('/compute', methods=['POST'])
    def compute():
        response = ""

        value = request.form.get("data")
        if not value:
            value = ""

        payload = value.encode('utf-8')

        if len(payload) == 0:
            return 'empty'

        result = hashlib.md5(payload).hexdigest()

        response += f"Result {helpers.utils.escape_for_html(result)}"
        return response