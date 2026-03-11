from flask import request
from helpers.utils import escape_for_html
import helpers.request_wrapper
import helpers.utils


def load_handlers(app):

    @app.route('/exports/write', methods=['GET'])
    def write_export_get():
        return write_export_post()

    @app.route('/exports/write', methods=['POST'])
    def write_export_post():
        response_text = ""

        wrapper = helpers.request_wrapper.wrap(request)
        query_value = wrapper.get_query_value("export")
        if not query_value:
            query_value = ""

        store = {}
        store["primary"] = "fixed"
        store["dynamic"] = query_value
        store["other"] = "placeholder"

        export_name = store["dynamic"]

        fd = None

        try:
            target_file = f"{helpers.utils.TESTFILES_DIR}/{export_name}"
            fd = open(target_file, "wb")

            response_text += (
                f"Now ready to write to file: {escape_for_html(target_file)}"
            )

        except IOError as err:
            response_text += (
                f"Problem reading from file '{escape_for_html(target_file)}': "
                f"{escape_for_html(err.strerror)}"
            )

        finally:
            try:
                if fd is not None:
                    fd.close()
            except IOError:
                pass

        return response_text