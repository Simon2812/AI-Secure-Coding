from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def define_routes(app):

    @app.route('/media/read', methods=['GET'])
    def media_read_get():
        return media_read_post()

    @app.route('/media/read', methods=['POST'])
    def media_read_post():
        result = ""

        header_value = request.headers.get("media")
        if not header_value:
            header_value = ""

        builder = "prefix"
        builder += header_value
        builder += "suffix_marker"

        selected_name = builder[6:-13]

        if "../" in selected_name:
            result += "File name must not include '../'"
            return result

        file_path = None
        handle = None

        try:
            file_path = f"{helpers.utils.TESTFILES_DIR}/{selected_name}"
            handle = open(file_path, "rb")

            result += (
                f"The beginning of file: '{escape_for_html(file_path)}' is:\n\n"
                f"{escape_for_html(handle.read(1000).decode('utf-8'))}"
            )

        except IOError as error:
            result += (
                f"Problem reading from file '{file_path}': "
                f"{escape_for_html(error.strerror)}"
            )

        finally:
            try:
                if handle is not None:
                    handle.close()
            except IOError:
                pass

        return result