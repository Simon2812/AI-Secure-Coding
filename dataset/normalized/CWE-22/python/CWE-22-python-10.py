from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import helpers.request_wrapper
import base64


def mount_routes(app):

    @app.route('/logs/view', methods=['GET'])
    def view_log_get():
        return view_log_post()

    @app.route('/logs/view', methods=['POST'])
    def view_log_post():
        result = ""

        wrapper = helpers.request_wrapper.wrap(request)
        value = wrapper.get_form_value("file")
        if not value:
            value = ""

        encoded = base64.b64encode(value.encode("utf-8"))
        decoded = base64.b64decode(encoded).decode("utf-8")

        file_name = None
        handle = None

        try:
            file_name = f"{helpers.utils.TESTFILES_DIR}/{decoded}"
            handle = open(file_name, "rb")

            result += (
                f"The beginning of file: '{escape_for_html(file_name)}' is:\n\n"
                f"{escape_for_html(handle.read(1000).decode('utf-8'))}"
            )

        except IOError as e:
            result += (
                f"Problem reading from file '{file_name}': "
                f"{escape_for_html(e.strerror)}"
            )

        finally:
            try:
                if handle is not None:
                    handle.close()
            except IOError:
                pass

        return result