from flask import request
from helpers.utils import escape_for_html
import platform
import codecs
import helpers.utils
from urllib.parse import urlparse
from urllib.request import url2pathname


def initialize(app):

    @app.route('/archives/open', methods=['GET'])
    def open_archive_get():
        return open_archive_post()

    @app.route('/archives/open', methods=['POST'])
    def open_archive_post():
        result = ""

        header_value = request.headers.get("file")
        if not header_value:
            header_value = ""

        storage = {}
        storage["first"] = "fixed"
        storage["second"] = header_value
        storage["third"] = "other"

        entry_name = storage["second"]

        start_slashes = ""
        if platform.system() == "Windows":
            start_slashes = "/"
        else:
            start_slashes = "//"

        try:
            uri = urlparse(
                "file:" + start_slashes +
                helpers.utils.TESTFILES_DIR.replace("\\", "/").replace(" ", "_") +
                entry_name
            )

            handle = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{entry_name}",
                "r",
                "utf-8"
            )

            result += (
                f"Access to file '{escape_for_html(handle.name)}' created."
            )
            result += " And file already exists."

        except FileNotFoundError:
            result += " But file doesn't exist yet."
        except IOError:
            pass

        return results