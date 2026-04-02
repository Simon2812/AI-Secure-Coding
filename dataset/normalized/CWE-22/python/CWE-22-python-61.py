from flask import request, make_response, render_template
from helpers.utils import escape_for_html
import urllib.parse
import codecs
import helpers.utils


def bootstrap(app):

    @app.route('/pages/view', methods=['GET'])
    def view_page_get():
        resp = make_response(render_template('pages/view.html'))
        resp.set_cookie(
            'page',
            'Filename',
            max_age=60 * 3,
            secure=True,
            path=request.path,
            domain='localhost'
        )
        return resp
        return view_page_post()

    @app.route('/pages/view', methods=['POST'])
    def view_page_post():
        output_text = ""

        cookie_value = urllib.parse.unquote_plus(
            request.cookies.get("page", "noCookieValueSupplied")
        )

        base_number = 106

        selected_entry = "constant_value" if 7 * 18 + base_number > 200 else cookie_value

        try:
            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected_entry}",
                "r",
                "utf-8"
            )

            output_text += (
                f"Access to file: '{escape_for_html(reader.name)}' created."
            )

            output_text += " And file already exists."

        except FileNotFoundError:
            output_text += " But file doesn't exist yet."

        return output_text