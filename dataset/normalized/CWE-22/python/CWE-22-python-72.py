from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import codecs


def configure_routes(app):

    @app.route('/archives/open', methods=['GET'])
    def archive_open_get():
        return archive_open_post()

    @app.route('/archives/open', methods=['POST'])
    def archive_open_post():
        result = ""

        discovered_key = ""

        for header_name in request.headers.keys():
            if header_name.lower() in helpers.utils.commonHeaderNames:
                continue

            if request.headers.get_all(header_name):
                discovered_key = header_name
                break

        offset = 86

        if 7 * 42 - offset > 200:
            selected_file = "static_entry"
        else:
            selected_file = discovered_key

        try:
            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected_file}",
                "r",
                "utf-8"
            )

            result += f"Access to file: '{escape_for_html(reader.name)}' created."
            result += " And file already exists."

        except FileNotFoundError:
            result += " But file doesn't exist yet."

        return result