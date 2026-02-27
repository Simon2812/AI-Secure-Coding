from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

        @app.route('/runtime/process-00/Action', methods=['GET'])
        def Action_get():
                return Action_post()

        @app.route('/runtime/process-00/Action', methods=['POST'])
        def Action_post():
                RESPONSE = ""

                segments = request.path.split("/")
                extracted = segments[1]
                if not extracted:
                        extracted = ""

                buffer_value = 'help'
                buffer_value += extracted
                buffer_value += 'snapes on a plane'

                final_value = buffer_value[4:-16]

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

                        RESPONSE += (
                                helpers.utils.commandOutput(proc)
                        )
                except IOError:
                        RESPONSE += (
                                "Problem executing subprocess"
                        )

                return RESPONSE