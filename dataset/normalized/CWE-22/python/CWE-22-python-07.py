from flask import request
from helpers.utils import escape_for_html
import codecs
import helpers.utils


def register_routes(app):

    @app.route('/assets/open', methods=['GET'])
    def open_asset_get():
        return open_asset_post()

    @app.route('/assets/open', methods=['POST'])
    def open_asset_post():
        result = ""

        values = request.form.getlist("asset")
        user_value = ""
        if values:
            user_value = values[0]

        storage = {}
        storage["primary"] = "default"
        storage["secondary"] = user_value
        storage["other"] = "placeholder"

        file_name = storage["secondary"]

        try:
            handle = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{file_name}",
                "r",
                "utf-8"
            )

            result += (
                f"Access to file '{escape_for_html(handle.name)}' created."
            )
            result += " And file already exists."

        except FileNotFoundError:
            result += " But file doesn't exist yet."

        return result