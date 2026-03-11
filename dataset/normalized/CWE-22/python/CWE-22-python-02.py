from flask import request, make_response, render_template
import urllib.parse
import codecs
import os
from helpers.utils import escape_for_html
import helpers.utils
from helpers.factory import ProcessorFactory


def configure_routes(app):

    @app.route('/documents/open', methods=['GET'])
    def open_document_get():
        response = make_response(render_template('documents/open.html'))
        response.set_cookie(
            'document',
            'example.txt',
            max_age=180,
            secure=True,
            path=request.path,
            domain='localhost'
        )
        return response

    @app.route('/documents/open', methods=['POST'])
    def open_document_post():
        result = ""

        value = urllib.parse.unquote_plus(
            request.cookies.get("document", "default.txt")
        )

        processor = ProcessorFactory.create()
        candidate = processor.process(value)

        try:
            handle = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{candidate}",
                "r",
                "utf-8"
            )

            result += (
                f"Access to file '{escape_for_html(handle.name)}' created."
            )
            result += " And file already exists."

        except FileNotFoundError:
            result += " But file doesn't exist yet."

        return result