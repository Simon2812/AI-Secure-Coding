from flask import request
from helpers.utils import escape_for_html
import base64
import helpers.utils


def initialize(app):

    @app.route('/media/view', methods=['GET'])
    def view_media_get():
        return view_media_post()

    @app.route('/media/view', methods=['POST'])
    def view_media_post():
        output = ""

        query_items = request.args.getlist("media")
        raw_value = ""
        if query_items:
            raw_value = query_items[0]

        encoded = base64.b64encode(raw_value.encode("utf-8"))
        decoded_name = base64.b64decode(encoded).decode("utf-8")

        file_path = None
        handle = None

        try:
            file_path = f"{helpers.utils.TESTFILES_DIR}/{decoded_name}"

            with open(file_path, "rb") as handle:
                output += (
                    f"The beginning of file '{escape_for_html(file_path)}' is:\n\n"
                    f"{escape_for_html(handle.read(1000).decode('utf-8'))}"
                )

        except IOError as err:
            output += (
                f"Problem reading from file '{file_path}': "
                f"{escape_for_html(err.strerror)}"
            )

        return output