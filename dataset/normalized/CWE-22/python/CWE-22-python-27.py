from flask import request
from helpers.utils import escape_for_html
import urllib.parse
import codecs
import helpers.utils


def register_routes(app):

    @app.route('/archives/load', methods=['GET'])
    def load_archive_get():
        return load_archive_post()

    @app.route('/archives/load', methods=['POST'])
    def load_archive_post():
        reply = ""

        raw_query = request.query_string.decode("utf-8")

        index = raw_query.find("archive" + "=")
        if index == -1:
            return "request.query_string did not contain expected parameter 'archive'."

        value = raw_query[index + len("archive") + 1:]

        amp = value.find("&")
        if amp != -1:
            value = value[:amp]

        value = urllib.parse.unquote_plus(value)

        selected = ""
        if value:
            items = []
            items.append("default")
            items.append(value)
            items.append("placeholder")
            items.pop(0)
            selected = items[0]

        try:
            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected}",
                "r",
                "utf-8"
            )

            reply += f"Access to file '{escape_for_html(reader.name)}' created."
            reply += " And file already exists."

        except FileNotFoundError:
            reply += " But file doesn't exist yet."

        return reply