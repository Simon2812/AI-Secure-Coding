from flask import request
from helpers.utils import escape_for_html
import pathlib
import helpers.utils


def define_routes(app):

    @app.route('/themes/read', methods=['GET'])
    def read_theme_get():
        return read_theme_post()

    @app.route('/themes/read', methods=['POST'])
    def read_theme_post():
        body = ""

        selected_key = ""

        for field in request.form.keys():
            if "theme" in request.form.getlist(field):
                selected_key = field
                break

        try:
            base_dir = pathlib.Path(helpers.utils.TESTFILES_DIR)
            target_path = base_dir / selected_key

            body += (
                f"The beginning of file '{escape_for_html(str(target_path))}' is:\n\n"
                f"{escape_for_html(target_path.read_text()[:1000])}"
            )

        except OSError as err:
            body += (
                f"Problem reading from file '{escape_for_html(str(target_path))}': "
                f"{escape_for_html(err.strerror)}"
            )

        return body