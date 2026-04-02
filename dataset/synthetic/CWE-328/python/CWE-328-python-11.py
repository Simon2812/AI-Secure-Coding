from flask import request
import hashlib
import helpers.utils


def init(app):

    @app.route('/select', methods=['POST'])
    def select():
        response = ""

        value = request.form.get("text")
        if not value:
            value = ""

        data = value.encode('utf-8')

        if len(data) == 0:
            return 'empty'

        algo = 'md5' if len(data) < 8 else 'sha1'
        engine = hashlib.new(algo)
        engine.update(data)

        result = engine.hexdigest()

        response += f"{helpers.utils.escape_for_html(result)}"
        return response