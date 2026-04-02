from flask import request
from helpers.utils import escape_for_html
import os
import helpers.utils


def setup(app):

    @app.route('/configs/check', methods=['GET'])
    def check_config_get():
        return check_config_post()

    @app.route('/configs/check', methods=['POST'])
    def check_config_post():
        result = ""

        key_name = ""
        for field in request.form.keys():
            if "config" in request.form.getlist(field):
                key_name = field
                break

        selected_item = ""
        if key_name:
            buffer = []
            buffer.append("safe")
            buffer.append(key_name)
            buffer.append("other")
            buffer.pop(0)
            selected_item = buffer[0]

        path_candidate = f"{helpers.utils.TESTFILES_DIR}/{selected_item}"

        if os.path.exists(path_candidate):
            result += f"File '{escape_for_html(path_candidate)}' exists."
        else:
            result += f"File '{escape_for_html(path_candidate)}' does not exist."

        return result