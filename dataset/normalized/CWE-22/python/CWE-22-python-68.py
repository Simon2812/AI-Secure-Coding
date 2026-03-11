from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import platform
import codecs
from urllib.parse import urlparse


def bind_endpoints(app):

    @app.route('/configs/open', methods=['GET'])
    def config_open_get():
        return config_open_post()

    @app.route('/configs/open', methods=['POST'])
    def config_open_post():
        result = ""

        detected_key = ""
        for field in request.form.keys():
            if "config" in request.form.getlist(field):
                detected_key = field
                break

        offset = 86

        if 7 * 42 - offset > 200:
            selected_item = "static_file"
        else:
            selected_item = detected_key

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
                selected_item
            )

            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected_item}",
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