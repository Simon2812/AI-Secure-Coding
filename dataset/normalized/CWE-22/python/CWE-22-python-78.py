from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import helpers.separate_request


def bind_endpoints(app):

    @app.route('/documents/preview', methods=['GET'])
    def document_preview_get():
        return document_preview_post()

    @app.route('/documents/preview', methods=['POST'])
    def document_preview_post():
        result = ""

        wrapper = helpers.separate_request.request_wrapper(request)
        incoming_value = wrapper.get_safe_value("document")

        storage = {}
        storage["primary"] = "default_doc"
        storage["secondary"] = incoming_value
        storage["tertiary"] = "unused_doc"

        selected_name = "default_doc"
        selected_name = storage["secondary"]
        selected_name = storage["primary"]

        file_path = None
        reader = None

        try:
            file_path = f"{helpers.utils.TESTFILES_DIR}/{selected_name}"
            reader = open(file_path, "rb")

            result += (
                f"The beginning of file: '{escape_for_html(file_path)}' is:\n\n"
                f"{escape_for_html(reader.read(1000).decode('utf-8'))}"
            )

        except IOError as error:
            result += (
                f"Problem reading from file '{file_path}': "
                f"{escape_for_html(error.strerror)}"
            )

        finally:
            try:
                if reader is not None:
                    reader.close()
            except IOError:
                pass

        return result