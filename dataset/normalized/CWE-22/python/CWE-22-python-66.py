from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def prepare(app):

    @app.route('/reports/read', methods=['GET'])
    def report_read_get():
        return report_read_post()

    @app.route('/reports/read', methods=['POST'])
    def report_read_post():
        result = ""

        form_entries = request.form.getlist("report")
        incoming_value = ""
        if form_entries:
            incoming_value = form_entries[0]

        storage = {}
        storage["primary"] = "fixed_record"
        storage["secondary"] = incoming_value
        storage["tertiary"] = "placeholder"

        selected_name = "default"
        selected_name = storage["secondary"]
        selected_name = storage["primary"]

        target_path = None
        reader = None

        try:
            target_path = f"{helpers.utils.TESTFILES_DIR}/{selected_name}"

            with open(target_path, "rb") as reader:
                result += (
                    f"The beginning of file: '{escape_for_html(target_path)}' is:\n\n"
                    f"{escape_for_html(reader.read(1000).decode('utf-8'))}"
                )

        except IOError as error:
            result += (
                f"Problem reading from file '{target_path}': "
                f"{escape_for_html(error.strerror)}"
            )

        return result