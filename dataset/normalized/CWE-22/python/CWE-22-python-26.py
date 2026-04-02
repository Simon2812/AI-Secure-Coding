from flask import request
from helpers.utils import escape_for_html
import helpers.separate_request
import helpers.ThingFactory
import helpers.utils
import os


def prepare(app):

    @app.route('/packages/check', methods=['GET'])
    def check_package_get():
        return check_package_post()

    @app.route('/packages/check', methods=['POST'])
    def check_package_post():
        message = ""

        wrapper = helpers.separate_request.request_wrapper(request)
        incoming = wrapper.get_query_parameter("package")
        if not incoming:
            incoming = ""

        processor = helpers.ThingFactory.createThing()
        package_name = processor.doSomething(incoming)

        file_path = f"{helpers.utils.TESTFILES_DIR}/{package_name}"

        if os.path.exists(file_path):
            message += f"File '{escape_for_html(file_path)}' exists."
        else:
            message += f"File '{escape_for_html(file_path)}' does not exist."

        return message