from flask import request
from helpers.utils import escape_for_html
import pathlib
import helpers.utils


def define_routes(app):

    @app.route('/reports/preview', methods=['GET'])
    def preview_report_get():
        return preview_report_post()

    @app.route('/reports/preview', methods=['POST'])
    def preview_report_post():
        result = ""

        values = request.form.getlist("report")
        input_value = ""
        if values:
            input_value = values[0]

        prefix = "start"
        prefix += input_value
        prefix += "finish"
        name = prefix[5:-6]

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