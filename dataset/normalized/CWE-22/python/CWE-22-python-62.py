from flask import request, make_response, render_template
from helpers.utils import escape_for_html
import urllib.parse
import pathlib
import helpers.utils


def configure_routes(app):

    @app.route('/assets/view', methods=['GET'])
    def asset_view_get():
        resp = make_response(render_template('assets/view.html'))
        resp.set_cookie(
            'asset',
            'FileName',
            max_age=60 * 3,
            secure=True,
            path=request.path,
            domain='localhost'
        )
        return resp
        return asset_view_post()

    @app.route('/assets/view', methods=['POST'])
    def asset_view_post():
        message_buffer = ""

        cookie_input = urllib.parse.unquote_plus(
            request.cookies.get("asset", "noCookieValueSupplied")
        )

        selected_file = cookie_input

        try:
            base_dir = pathlib.Path(helpers.utils.TESTFILES_DIR)
            candidate = (base_dir / selected_file).resolve()

            if not str(candidate).startswith(str(base_dir)):
                message_buffer += "Invalid Path."
                return message_buffer

            message_buffer += (
                f"The beginning of file '{escape_for_html(str(candidate))}' is:\n\n"
                f"{escape_for_html(candidate.read_text()[:1000])}"
            )

        except OSError as err:
            message_buffer += (
                f"Problem reading from file '{escape_for_html(str(candidate))}': "
                f"{escape_for_html(err.strerror)}"
            )

        return message_buffer