from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def bootstrap(app):

    @app.route('/profiles/create', methods=['GET'])
    def profile_create_get():
        return profile_create_post()

    @app.route('/profiles/create', methods=['POST'])
    def profile_create_post():
        result = ""

        header_items = request.headers.getlist("profile")
        received_value = ""

        if header_items:
            received_value = header_items[0]

        options = "XYZ"
        selector = options[1]

        match selector:
            case "X":
                chosen_name = received_value
            case "Y":
                chosen_name = "default_profile"
            case "Z" | "W":
                chosen_name = received_value
            case _:
                chosen_name = "fallback_value"

        try:
            destination = f"{helpers.utils.TESTFILES_DIR}/{chosen_name}"

            with open(destination, "wb") as writer:
                result += (
                    f"Now ready to write to file: {escape_for_html(destination)}"
                )

        except IOError as error:
            result += (
                f"Problem reading from file '{escape_for_html(destination)}': "
                f"{escape_for_html(error.strerror)}"
            )

        return results