from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def bind_endpoints(app):

    @app.route('/documents/preview', methods=['GET'])
    def preview_document_get():
        return preview_document_post()

    @app.route('/documents/preview', methods=['POST'])
    def preview_document_post():
        result = ""

        header_list = request.headers.getlist("document")
        header_value = ""
        if header_list:
            header_value = header_list[0]

        container = {}
        container["first"] = "fixed"
        container["second"] = header_value
        container["third"] = "other"

        document_name = container["second"]

        path_value = None

        try:
            path_value = f"{helpers.utils.TESTFILES_DIR}/{document_name}"

            with open(path_value, "rb") as reader:
                result += (
                    f"The beginning of file '{escape_for_html(path_value)}' is:\n\n"
                    f"{escape_for_html(reader.read(1000).decode('utf-8'))}"
                )

        except IOError as e:
            result += (
                f"Problem reading from file '{path_value}': "
                f"{escape_for_html(e.strerror)}"
            )

        return result