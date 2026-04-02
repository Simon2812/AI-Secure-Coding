from flask import request
from helpers.utils import escape_for_html
import codecs
import helpers.utils


def define_routes(app):

    @app.route('/themes/load', methods=['GET'])
    def load_theme_get():
        return load_theme_post()

    @app.route('/themes/load', methods=['POST'])
    def load_theme_post():
        result = ""

        header_name = ""

        for header in request.headers.keys():
            if header.lower() in helpers.utils.commonHeaderNames:
                continue

            if request.headers.get_all(header):
                header_name = header
                break

        selected_name = "default"
        if "default" in selected_name:
            selected_name = header_name

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