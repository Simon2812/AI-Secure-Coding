from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import codecs


def initialize(app):

    @app.route('/records/open', methods=['GET'])
    def record_open_get():
        return record_open_post()

    @app.route('/records/open', methods=['POST'])
    def record_open_post():
        result = ""

        query_values = request.args.getlist("record")
        provided_value = ""

        if query_values:
            provided_value = query_values[0]

        options = "XYZ"
        selector = options[1]

        match selector:
            case "X":
                selected_file = provided_value
            case "Y":
                selected_file = "static_record"
            case "Z" | "W":
                selected_file = provided_value
            case _:
                selected_file = "fallback_record"

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