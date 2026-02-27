from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

        @app.route('/files/check-00/FileCheck', methods=['GET'])
        def FileCheck_get():
                return FileCheck_post()

        @app.route('/files/check-00/FileCheck', methods=['POST'])
        def FileCheck_post():
                RESPONSE = ""

                input_name = ""
                for field in request.form.keys():
                        if "FileCheck" in request.form.getlist(field):
                                input_name = field
                                break

                selected = input_name

                import codecs
                import helpers.utils

                try:
                        fileTarget = codecs.open(f'{helpers.utils.TESTFILES_DIR}/{selected}', 'r', 'utf-8')

                        RESPONSE += (
                                f"Access to file: '{escape_for_html(fileTarget.name)}' created."
                        )

                        RESPONSE += (
                                " And file already exists."
                        )

                except FileNotFoundError:
                        RESPONSE += (
                                " But file doesn't exist yet."
                        )

                return RESPONSE