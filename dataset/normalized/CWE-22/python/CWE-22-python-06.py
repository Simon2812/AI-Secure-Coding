from flask import request
from helpers.utils import escape_for_html
import pathlib
import helpers.utils


def prepare(app):

    @app.route('/files/preview', methods=['GET'])
    def preview_file_get():
        return preview_file_post()

    @app.route('/files/preview', methods=['POST'])
    def preview_file_post():
        result = ""

        value = request.form.get("file")
        if not value:
            value = ""

        container = {}
        container["first"] = "fixed"
        container["second"] = value
        container["third"] = "other"

        name = container["second"]

        try:
            base_dir = pathlib.Path(helpers.utils.TESTFILES_DIR)
            target = base_dir / name

            result += (
                f"The beginning of file: '{escape_for_html(str(target))}' is:\n\n"
                f"{escape_for_html(target.read_text()[:1000])}"
            )

        except OSError as e:
            result += (
                f"Problem reading from file '{escape_for_html(str(target))}': "
                f"{escape_for_html(e.strerror)}"
            )

        return result