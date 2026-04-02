from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import urllib.parse
import platform
import codecs
from urllib.parse import urlparse


def prepare(app):

    @app.route('/storage/view', methods=['GET'])
    def storage_view_get():
        return storage_view_post()

    @app.route('/storage/view', methods=['POST'])
    def storage_view_post():
        result = ""

        raw_query = request.query_string.decode("utf-8")

        key_position = raw_query.find("item" + "=")
        if key_position == -1:
            return "request.query_string did not contain expected parameter 'item'."

        extracted_value = raw_query[key_position + len("item") + 1:]

        separator = extracted_value.find("&")
        if separator != -1:
            extracted_value = extracted_value[:separator]

        extracted_value = urllib.parse.unquote_plus(extracted_value)

        selected_entry = "static_item"

        if extracted_value:
            buffer = []
            buffer.append("alpha")
            buffer.append(extracted_value)
            buffer.append("omega")
            buffer.pop(0)

            selected_entry = buffer[1]

        prefix = ""

        if platform.system() == "Windows":
            prefix = "/"
        else:
            prefix = "//"

        try:
            file_uri = urlparse(
                "file:"
                + prefix
                + helpers.utils.TESTFILES_DIR.replace("\\", "/").replace(" ", "_")
                + selected_entry
            )

            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected_entry}",
                "r",
                "utf-8"
            )

            result += f"Access to file: '{escape_for_html(reader.name)}' created."
            result += " And file already exists."

        except FileNotFoundError:
            result += " But file doesn't exist yet."
        except IOError:
            pass

        return result