from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import helpers.request_wrapper


def bootstrap(app):

    @app.route('/exports/save', methods=['GET'])
    def save_export_get():
        return save_export_post()

    @app.route('/exports/save', methods=['POST'])
    def save_export_post():
        result = ""

        wrapper = helpers.request_wrapper.wrap(request)
        value = wrapper.get_form_value("name")
        if not value:
            value = ""

        selected = ""
        if value:
            items = []
            items.append("safe")
            items.append(value)
            items.append("other")
            items.pop(0)
            selected = items[0]

        try:
            file_path = f"{helpers.utils.TESTFILES_DIR}/{selected}"
            with open(file_path, "wb") as handle:
                result += (
                    f"Now ready to write to file: {escape_for_html(file_path)}"
                )

        except IOError as e:
            result += (
                f"Problem reading from file '{escape_for_html(file_path)}': "
                f"{escape_for_html(e.strerror)}"
            )

        return result