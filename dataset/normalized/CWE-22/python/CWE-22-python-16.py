from flask import request
from helpers.utils import escape_for_html
import platform
import codecs
import helpers.utils
from urllib.parse import urlparse
from urllib.request import url2pathname


def prepare(app):

    @app.route('/datasets/load', methods=['GET'])
    def load_dataset_get():
        return load_dataset_post()

    @app.route('/datasets/load', methods=['POST'])
    def load_dataset_post():
        result = ""

        value = ""
        header_values = request.headers.getlist("dataset")
        if header_values:
            value = header_values[0]

        options = "ABC"
        selector = options[0]

        match selector:
            case 'A':
                selected = value
            case 'B':
                selected = "default"
            case 'C' | 'D':
                selected = value
            case _:
                selected = "fallback"

        start_slashes = ""
        if platform.system() == "Windows":
            start_slashes = "/"
        else:
            start_slashes = "//"

        try:
            uri = urlparse(
                "file:" + start_slashes +
                helpers.utils.TESTFILES_DIR.replace("\\", "/").replace(" ", "_") +
                selected
            )

            reader = codecs.open(
                f"{helpers.utils.TESTFILES_DIR}/{selected}",
                "r",
                "utf-8"
            )

            result += (
                f"Access to file '{escape_for_html(reader.name)}' created."
            )
            result += " And file already exists."

        except FileNotFoundError:
            result += " But file doesn't exist yet."
        except IOError:
            pass

        return result