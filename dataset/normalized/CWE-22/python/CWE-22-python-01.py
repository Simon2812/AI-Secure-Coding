from flask import request, make_response, render_template
import urllib.parse
import codecs
import os
from helpers.utils import escape_for_html
import helpers.utils


def mount_routes(app):

    @app.route('/files/view', methods=['GET'])
    def view_file_get():
        response = make_response(render_template('files/view.html'))
        response.set_cookie(
            'file',
            'example.txt',
            max_age=180,
            secure=True,
            path=request.path,
            domain='localhost'
        )
        return response

    @app.route('/files/view', methods=['POST'])
    def view_file_post():
        response_text = ""

        value = urllib.parse.unquote_plus(
            request.cookies.get("file", "default.txt")
        )

        name = value

        try:
            f = codecs.open(f"{helpers.utils.TESTFILES_DIR}/{name}", "r", "utf-8")

            response_text += (
                f"Access to file '{escape_for_html(f.name)}' created."
            )

            response_text += " And file already exists."

        except FileNotFoundError:
            response_text += " But file doesn't exist yet."

        return response_text