from flask import request
from helpers.utils import escape_for_html
import helpers.utils
import helpers.factory


def bind_endpoints(app):

    @app.route('/uploads/write', methods=['GET'])
    def write_entry_get():
        return write_entry_post()

    @app.route('/uploads/write', methods=['POST'])
    def write_entry_post():
        result = ""

        values = request.form.getlist("name")
        value = ""
        if values:
            value = values[0]

        processor = helpers.factory.create()
        entry = processor.process(value)

        fd = None

        try:
            path_value = f"{helpers.utils.TESTFILES_DIR}/{entry}"
            fd = open(path_value, "wb")

            result += (
                f"Now ready to write to file: {escape_for_html(path_value)}"
            )

        except IOError as e:
            result += (
                f"Problem reading from file '{escape_for_html(path_value)}': "
                f"{escape_for_html(e.strerror)}"
            )

        finally:
            try:
                if fd is not None:
                    fd.close()
            except IOError:
                pass

        return result