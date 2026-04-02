from flask import request
from helpers.utils import escape_for_html
import pathlib
import helpers.utils


def initialize(app):

    @app.route('/documents/preview', methods=['GET'])
    def document_preview_get():
        return document_preview_post()

    @app.route('/documents/preview', methods=['POST'])
    def document_preview_post():
        reply_text = ""

        submitted_value = request.form.get("document")
        if not submitted_value:
            submitted_value = ""

        marker = "This should never happen"

        if "should" not in marker:
            chosen_name = "fallback_value"
        else:
            chosen_name = submitted_value

        try:
            base_path = pathlib.Path(helpers.utils.TESTFILES_DIR)
            resolved_target = (base_path / chosen_name).resolve()

            if not str(resolved_target).startswith(str(base_path)):
                reply_text += "Invalid Path."
                return reply_text

            reply_text += (
                f"The beginning of file '{escape_for_html(str(resolved_target))}' is:\n\n"
                f"{escape_for_html(resolved_target.read_text()[:1000])}"
            )

        except OSError as error:
            reply_text += (
                f"Problem reading from file '{escape_for_html(str(resolved_target))}': "
                f"{escape_for_html(error.strerror)}"
            )

        return reply_text