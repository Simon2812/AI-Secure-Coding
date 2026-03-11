from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def load_handlers(app):

    @app.route('/backups/create', methods=['GET'])
    def create_backup_get():
        return create_backup_post()

    @app.route('/backups/create', methods=['POST'])
    def create_backup_post():
        result = ""

        header_value = request.headers.get("backup")
        if not header_value:
            header_value = ""

        target_name = header_value

        try:
            output_path = f"{helpers.utils.TESTFILES_DIR}/{target_name}"
            with open(output_path, "wb") as writer:
                result += (
                    f"Now ready to write to file: {escape_for_html(output_path)}"
                )

        except IOError as e:
            result += (
                f"Problem reading from file '{escape_for_html(output_path)}': "
                f"{escape_for_html(e.strerror)}"
            )

        return result