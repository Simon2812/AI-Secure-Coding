from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

        @app.route('/ops/execute-01/user', methods=['GET'])
        def user_get():
                return user_post()

        @app.route('/ops/execute-01/user', methods=['POST'])
        def user_post():
                RESPONSE = ""

                input_value = request.args.get("user")
                if not input_value:
                        input_value = ""

                registry = {}
                registry['alpha'] = 'a-Value'
                registry['beta'] = input_value
                registry['gamma'] = 'another-Value'

                current = "safe!"
                current = registry['beta']
                current = registry['alpha']

                import platform
                import subprocess
                import helpers.utils

                execution_line = ""
                if platform.system() == "Windows":
                        execution_line = "cmd.exe /c "
                else:
                        execution_line = "sh -c "
                execution_line += f"echo {current}"

                try:
                        proc = subprocess.run(execution_line, shell=True, capture_output=True, encoding="utf-8")

                        RESPONSE += (
                                helpers.utils.commandOutput(proc)
                        )
                except IOError:
                        RESPONSE += (
                                "Problem executing subprocess"
                        )

                return RESPONSE