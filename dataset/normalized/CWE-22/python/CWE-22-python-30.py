from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def mount_routes(app):

    @app.route('/notes/save', methods=['GET'])
    def save_note_get():
        return save_note_post()

    @app.route('/notes/save', methods=['POST'])
    def save_note_post():
        content = ""

        header_value = request.headers.get("note")
        if not header_value:
            header_value = ""

        try:
            target = f"{helpers.utils.TESTFILES_DIR}/{header_value}"

            with open(target, "wb") as writer:
                content += (
                    f"Now ready to write to file: {escape_for_html(target)}"
                )

        except IOError as err:
            content += (
                f"Problem reading from file '{escape_for_html(target)}': "
                f"{escape_for_html(err.strerror)}"
            )

        return content