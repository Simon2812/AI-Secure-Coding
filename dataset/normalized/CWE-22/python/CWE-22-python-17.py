from flask import request
from helpers.utils import escape_for_html
import pathlib
import helpers.utils


def register_routes(app):

    @app.route('/packages/status', methods=['GET'])
    def package_status_get():
        return package_status_post()

    @app.route('/packages/status', methods=['POST'])
    def package_status_post():
        result = ""

        header_items = request.headers.getlist("package")
        value = ""
        if header_items:
            value = header_items[0]

        item_name = value

        base_path = pathlib.Path(helpers.utils.TESTFILES_DIR)
        target_path = base_path / item_name

        if target_path.exists():
            result += f"File '{escape_for_html(str(target_path))}' exists."
        else:
            result += f"File '{escape_for_html(str(target_path))}' does not exist."

        return result