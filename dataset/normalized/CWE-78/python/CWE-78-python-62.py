from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

        @app.route('/system/exec-00/Action350', methods=['GET'])
        def Action350_get():
                return Action350_post()

        @app.route('/system/exec-00/Action350', methods=['POST'])
        def Action350_post():
                RESPONSE = ""

                import helpers.separate_request

                wrapped = helpers.separate_request.request_wrapper(request)
                user_value = wrapped.get_form_parameter("Action350")
                if not user_value:
                        user_value = ""

                storage = {}
                storage['primary'] = 'a-Value'
                storage['secondary'] = user_value
                storage['tertiary'] = 'another-Value'

                result = "safe!"
                result = storage['secondary']
                result = storage['primary']

                import platform
                import subprocess
                import helpers.utils

                command_line = ""
                if platform.system() == "Windows":
                        command_line = "cmd.exe /c "
                else:
                        command_line = "sh -c "
                command_line += f"echo {result}"

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