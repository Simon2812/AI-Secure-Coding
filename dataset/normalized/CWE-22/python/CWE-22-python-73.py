from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def setup(app):

    @app.route('/datasets/read', methods=['GET'])
    def dataset_read_get():
        return dataset_read_post()

    @app.route('/datasets/read', methods=['POST'])
    def dataset_read_post():
        result = ""

        query_value = request.args.get("dataset")
        if not query_value:
            query_value = ""

        options = "XYZ"
        selector = options[1]

        match selector:
            case "X":
                selected_name = query_value
            case "Y":
                selected_name = "default_dataset"
            case "Z" | "W":
                selected_name = query_value
            case _:
                selected_name = "fallback_dataset"

        file_path = None
        reader = None

        try:
            file_path = f"{helpers.utils.TESTFILES_DIR}/{selected_name}"

            with open(file_path, "rb") as reader:
                result += (
                    f"The beginning of file: '{escape_for_html(file_path)}' is:\n\n"
                    f"{escape_for_html(reader.read(1000).decode('utf-8'))}"
                )

        except IOError as error:
            result += (
                f"Problem reading from file '{file_path}': "
                f"{escape_for_html(error.strerror)}"
            )

        return result