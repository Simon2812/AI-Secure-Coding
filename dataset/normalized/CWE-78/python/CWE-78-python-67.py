from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

        @app.route('/service/transform/Task1173', methods=['GET'])
        def Task1173_get():
                return Task1173_post()

        @app.route('/service/transform/Task1173', methods=['POST'])
        def Task1173_post():
                RESPONSE = ""

                import helpers.separate_request
                wrapper = helpers.separate_request.request_wrapper(request)
                input_value = wrapper.get_safe_value("Task1173")

                import base64
                encoded = base64.b64encode(input_value.encode('utf-8'))
                decoded_value = base64.b64decode(encoded).decode('utf-8')

                import platform
                import subprocess
                import helpers.utils

                command_line = ""
                if platform.system() == "Windows":
                        command_line = "cmd.exe /c "
                else:
                        command_line = "sh -c "
                command_line += f"echo {decoded_value}"

                try:
                        proc = subprocess.run(command_line, shell=True, capture_output=True, encoding="utf-8")

                        RESPONSE += (
                                helpers.utils.commandOutput(proc)
                        )
                except IOError:
                        RESPONSE += (
                                "Problem executing subprocess"
                        )

                return RESPONSE
