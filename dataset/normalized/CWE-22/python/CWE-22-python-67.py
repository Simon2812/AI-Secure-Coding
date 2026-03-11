from flask import request
from helpers.utils import escape_for_html
import helpers.separate_request
import helpers.utils
import os


def register_routes(app):

    @app.route('/logs/check', methods=['GET'])
    def log_check_get():
        return log_check_post()

    @app.route('/logs/check', methods=['POST'])
    def log_check_post():
        result = ""

        wrapper = helpers.separate_request.request_wrapper(request)
        submitted_value = wrapper.get_form_parameter("log")
        if not submitted_value:
            submitted_value = ""

        offset = 86

        if 7 * 42 - offset > 200:
            selected_entry = "static_entry"
        else:
            selected_entry = submitted_value

        target_location = f"{helpers.utils.TESTFILES_DIR}/{selected_entry}"

        if os.path.exists(target_location):
            result += f"File '{escape_for_html(target_location)}' exists."
        else:
            result += f"File '{escape_for_html(target_location)}' does not exist."

        return result