from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import platform
import codecs
from urllib.parse import urlparse


def mount_routes(app):

    @app.route('/images/open', methods=['GET'])
    def image_open_get():
        return image_open_post()

    @app.route('/images/open', methods=['POST'])
    def image_open_post():
        result = ""

        segments = request.path.split("/")
        selected_part = segments[1]

        if not selected_part:
            selected_part = ""

        prefix = ""

        if platform.system() == "Windows":
            prefix = "/"
        else:
            prefix = "//"

        try:
            file_uri = urlparse(
                "file:" +
                prefix +
                helpers.utils.TESTFILES_DIR.replace("\\", "/").replace(" ", "_") +
                selected_part
            )

            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected_part}",
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
