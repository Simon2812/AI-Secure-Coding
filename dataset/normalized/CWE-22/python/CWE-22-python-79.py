from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def define_routes(app):

    @app.route('/files/preview', methods=['GET'])
    def file_preview_get():
        return file_preview_post()

    @app.route('/files/preview', methods=['POST'])
    def file_preview_post():
        result = ""

        query_value = request.args.get("file")
        if not query_value:
            query_value = ""

        target_path = None
        handle = None

        if "../" in query_value:
            result += "File name must not include '../'"
            return result

        try:
            target_path = f"{helpers.utils.TESTFILES_DIR}/{query_value}"
            handle = open(target_path, "rb")

            result += (
                f"The beginning of file: '{escape_for_html(target_path)}' is:\n\n"
                f"{escape_for_html(handle.read(1000).decode('utf-8'))}"
            )

        except IOError as error:
            result += (
                f"Problem reading from file '{target_path}': "
                f"{escape_for_html(error.strerror)}"
            )

        finally:
            try:
                if handle is not None:
                    handle.close()
            except IOError:
                pass

        return result