from flask import request
import hashlib
import helpers.utils


def init(app):

    @app.route('/combine', methods=['POST'])
    def combine():
        output = ""

        text = request.form.get("value")
        if not text:
            text = ""

        data = text.encode('utf-8')

        if len(data) == 0:
            return 'empty'

        h1 = hashlib.md5(data).hexdigest()
        h2 = hashlib.sha1(data).hexdigest()

        combined = h1 + ":" + h2

        output += f"{helpers.utils.escape_for_html(combined)}"
        return output   