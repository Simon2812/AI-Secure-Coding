from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import base64
import codecs


def register_routes(app):

    @app.route('/assets/open', methods=['GET'])
    def asset_open_get():
        return asset_open_post()

    @app.route('/assets/open', methods=['POST'])
    def asset_open_post():
        result = ""

        segments = request.path.split("/")
        extracted_segment = segments[1]

        if not extracted_segment:
            extracted_segment = ""

        encoded_value = base64.b64encode(extracted_segment.encode("utf-8"))
        selected_name = base64.b64decode(encoded_value).decode("utf-8")

        try:
            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected_name}",
                "r",
                "utf-8"
            )

            result += f"Access to file: '{escape_for_html(reader.name)}' created."
            result += " And file already exists."

        except FileNotFoundError:
            result += " But file doesn't exist yet."

        return result