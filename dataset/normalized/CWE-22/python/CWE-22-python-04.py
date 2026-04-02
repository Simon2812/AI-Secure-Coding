from flask import request
from helpers.utils import escape_for_html
import helpers.utils


def initialize(app):

    @app.route('/storage/write', methods=['GET'])
    def write_file_get():
        return write_file_post()

    @app.route('/storage/write', methods=['POST'])
    def write_file_post():
        message = ""

        value = request.form.get("name")
        if not value:
            value = ""

        flag = "This should never happen"
        if 'should' not in flag:
            selected = "fallback.txt"
        else:
            selected = value

        fd = None

        try:
            path_value = f"{helpers.utils.TESTFILES_DIR}/{selected}"
            fd = open(path_value, "wb")

            message += (
                f"Now ready to write to file: {escape_for_html(path_value)}"
            )

        except IOError as e:
            message += (
                f"Problem reading from file '{escape_for_html(path_value)}': "
                f"{escape_for_html(e.strerror)}"
            )

        finally:
            try:
                if fd is not None:
                    fd.close()
            except IOError:
                pass

        return message