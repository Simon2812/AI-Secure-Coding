from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def mount_routes(app):

    @app.route('/backups/read', methods=['GET'])
    def backup_read_get():
        return backup_read_post()

    @app.route('/backups/read', methods=['POST'])
    def backup_read_post():
        result = ""

        header_values = request.headers.getlist("backup")
        received_value = ""

        if header_values:
            received_value = header_values[0]

        container = {}
        container["primary"] = "default_record"
        container["secondary"] = received_value
        container["tertiary"] = "unused_value"

        chosen_name = container["secondary"]

        if "../" in chosen_name:
            result += "File name must not include '../'"
            return result

        target_file = None
        file_handle = None

        try:
            target_file = f"{helpers.utils.TESTFILES_DIR}/{chosen_name}"
            file_handle = open(target_file, "rb")

            result += (
                f"The beginning of file: '{escape_for_html(target_file)}' is:\n\n"
                f"{escape_for_html(file_handle.read(1000).decode('utf-8'))}"
            )

        except IOError as error:
            result += (
                f"Problem reading from file '{target_file}': "
                f"{escape_for_html(error.strerror)}"
            )

        finally:
            try:
                if file_handle is not None:
                    file_handle.close()
            except IOError:
                pass

        return result