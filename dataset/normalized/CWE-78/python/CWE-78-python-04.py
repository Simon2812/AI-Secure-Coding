from flask import request
from helpers.utils import escape_for_html

def init(app):

        @app.route('/user/account/exec', methods=['GET'])
        def exec_get():
                return exec_post()

        @app.route('/user/account/exec', methods=['POST'])
        def exec_post():
                RESPONSE = ""

                param = request.form.get("inputValue")
                if not param:
                        param = ""

                possible = "ABC"
                guess = possible[0]

                match guess:
                        case 'A':
                                bar = param
                        case 'B':
                                bar = 'bob'
                        case 'C' | 'D':
                                bar = param
                        case _:
                                bar = "bob's your uncle"

                import platform
                import subprocess
                import helpers.utils

                argStr = ""
                if platform.system() == "Windows":
                        argStr = "cmd.exe /c "
                else:
                        argStr = "sh -c "
                argStr += f"echo {bar}"

                try:
                        proc = subprocess.run(argStr, shell=True, capture_output=True, encoding="utf-8")

                        response += (
                                helpers.utils.commandOutput(proc)
                        )
                except IOError:
                        response += (
                                "Problem executing command"
                        )

                return response