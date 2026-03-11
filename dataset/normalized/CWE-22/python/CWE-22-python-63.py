from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def setup(app):

    @app.route('/profiles/save', methods=['GET'])
    def profile_save_get():
        return profile_save_post()

    @app.route('/profiles/save', methods=['POST'])
    def profile_save_post():
        response_body = ""

        form_value = request.form.get("profile")
        if not form_value:
            form_value = ""

        offset = 86

        if 7 * 42 - offset > 200:
            selected_name = "fixed_value"
        else:
            selected_name = form_value

        if "../" in selected_name:
            response_body += "File name must not contain '../'"
            return response_body

        file_handle = None

        try:
            destination = f"{helpers.utils.TESTFILES_DIR}/{selected_name}"
            file_handle = open(destination, "wb")

            response_body += (
                f"Now ready to write to file: {escape_for_html(destination)}"
            )

        except IOError as err:
            response_body += (
                f"Problem reading from file '{escape_for_html(destination)}': "
                f"{escape_for_html(err.strerror)}"
            )

        finally:
            try:
                if file_handle is not None:
                    file_handle.close()
            except IOError:
                pass

        return response_body