from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import helpers.separate_request


def load_handlers(app):

    @app.route('/reports/create', methods=['GET'])
    def report_create_get():
        return report_create_post()

    @app.route('/reports/create', methods=['POST'])
    def report_create_post():
        result = ""

        wrapper = helpers.separate_request.request_wrapper(request)
        incoming_value = wrapper.get_query_parameter("report")
        if not incoming_value:
            incoming_value = ""

        variants = "XYZ"
        selector = variants[1]

        match selector:
            case "X":
                selected_name = incoming_value
            case "Y":
                selected_name = "default_report"
            case "Z" | "W":
                selected_name = incoming_value
            case _:
                selected_name = "fallback_report"

        file_path = None
        writer = None

        try:
            file_path = f"{helpers.utils.TESTFILES_DIR}/{selected_name}"
            writer = open(file_path, "wb")

            result += f"Now ready to write to file: {escape_for_html(file_path)}"

        except IOError as error:
            result += (
                f"Problem reading from file '{escape_for_html(file_path)}': "
                f"{escape_for_html(error.strerror)}"
            )

        finally:
            try:
                if writer is not None:
                    writer.close()
            except IOError:
                pass

        return result