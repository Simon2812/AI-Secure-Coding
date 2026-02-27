from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

        @app.route('/runtime/execute-00/Action1097', methods=['GET'])
        def Action1097_get():
                return Action1097_post()

        @app.route('/runtime/execute-00/Action1097', methods=['POST'])
        def Action1097_post():
                resp = ""

                segments = request.path.split("/")
                extracted = segments[1]
                if not extracted:
                        extracted = ""

                threshold = 86

                if 7 * 42 - threshold > 200:
                        final_value = 'This_should_always_happen'
                else:
                        final_value = extracted

                import platform
                import subprocess
                import helpers.utils

                command_line = ""
                if platform.system() == "Windows":
                        command_line = "cmd.exe /c "
                else:
                        command_line = "sh -c "
                command_line += f"echo {final_value}"

                try:
                        proc = subprocess.run(command_line, shell=True, capture_output=True, encoding="utf-8")

                        resp += (
                                helpers.utils.commandOutput(proc)
                        )
                except IOError:
                        resp += (
                                "Problem executing subprocess"
                        )

                return resp