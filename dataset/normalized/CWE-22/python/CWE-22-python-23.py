from flask import request
from helpers.utils import escape_for_html
import codecs
import helpers.utils


def setup(app):

    @app.route('/layouts/open', methods=['GET'])
    def open_layout_get():
        return open_layout_post()

    @app.route('/layouts/open', methods=['POST'])
    def open_layout_post():
        result = ""

        query_values = request.args.getlist("layout")
        value = ""
        if query_values:
            value = query_values[0]

        options = "XYZ"
        selector = options[0]

        match selector:
            case "X":
                selected_layout = value
            case "Y":
                selected_layout = "default"
            case "Z" | "W":
                selected_layout = value
            case _:
                selected_layout = "fallback"

        try:
            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected_layout}",
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