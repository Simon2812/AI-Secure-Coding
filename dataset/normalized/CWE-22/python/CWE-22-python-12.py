from flask import request
from helpers.utils import escape_for_html
import codecs
import helpers.utils


def configure_routes(app):

    @app.route('/templates/open', methods=['GET'])
    def open_template_get():
        return open_template_post()

    @app.route('/templates/open', methods=['POST'])
    def open_template_post():
        result = ""

        candidate = ""
        for key in request.form.keys():
            if "template" in request.form.getlist(key):
                candidate = key
                break

        selected_name = candidate

        try:
            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected_name}",
                "r",
                "utf-8"
            )

            result += (
                f"Access to file '{escape_for_html(reader.name)}' created."
            )
            result += " And file already exists."

        except FileNotFoundError:
            result += " But file doesn't exist yet."

        return result