from flask import request
from helpers.utils import escape_for_html
import pathlib
import helpers.utils


def load_handlers(app):

    @app.route('/records/check', methods=['GET'])
    def check_record_get():
        return check_record_post()

    @app.route('/records/check', methods=['POST'])
    def check_record_post():
        result = ""

        value = request.form.get("entry")
        if not value:
            value = ""

        data = {}
        data["alpha"] = "static"
        data["beta"] = value
        data["gamma"] = "other"

        chosen = data["beta"]

        root = pathlib.Path(helpers.utils.TESTFILES_DIR)
        location = root / chosen

        if location.exists():
            result += f"File '{escape_for_html(str(location))}' exists."
        else:
            result += f"File '{escape_for_html(str(location))}' does not exist."

        return result