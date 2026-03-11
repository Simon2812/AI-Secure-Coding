from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def bootstrap(app):

    @app.route('/images/preview', methods=['GET'])
    def preview_image_get():
        return preview_image_post()

    @app.route('/images/preview', methods=['POST'])
    def preview_image_post():
        result = ""

        query_value = request.args.get("image")
        if not query_value:
            query_value = ""

        container = {}
        container["alpha"] = "static"
        container["beta"] = query_value
        container["gamma"] = "other"

        image_name = container["beta"]

        file_path = None
        reader = None

        try:
            file_path = f"{helpers.utils.TESTFILES_DIR}/{image_name}"
            reader = open(file_path, "rb")

            result += (
                f"The beginning of file '{escape_for_html(file_path)}' is:\n\n"
                f"{escape_for_html(reader.read(1000).decode('utf-8'))}"
            )

        except IOError as e:
            result += (
                f"Problem reading from file '{file_path}': "
                f"{escape_for_html(e.strerror)}"
            )

        finally:
            try:
                if reader is not None:
                    reader.close()
            except IOError:
                pass

        return result