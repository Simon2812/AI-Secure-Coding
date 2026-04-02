from flask import request, make_response, render_template
from helpers.utils import escape_for_html
import urllib.parse
import pathlib
import helpers.utils


def setup(app):

    @app.route('/resources/check', methods=['GET'])
    def resource_check_get():
        response = make_response(render_template('resources/check.html'))
        response.set_cookie(
            'resource',
            'example.txt',
            max_age=180,
            secure=True,
            path=request.path,
            domain='localhost'
        )
        return response

    @app.route('/resources/check', methods=['POST'])
    def resource_check_post():
        message = ""

        raw_value = urllib.parse.unquote_plus(
            request.cookies.get("resource", "default.txt")
        )

        flag = "This should never happen"
        if 'should' not in flag:
            selected = "fallback.txt"
        else:
            selected = raw_value

        base = pathlib.Path(helpers.utils.TESTFILES_DIR)
        target = base / selected

        if target.exists():
            message += f"File '{escape_for_html(str(target))}' exists."
        else:
            message += f"File '{escape_for_html(str(target))}' does not exist."

        return message