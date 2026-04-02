from flask import request
from helpers.utils import escape_for_html

def init(app):

        @app.route('/tools/system/execute-165', methods=['GET'])
        def execute_165_get():
                return execute_165_post()

        @app.route('/tools/system/execute-165', methods=['POST'])
        def execute_165_post():
                RESPONSE = ""

                param = request.form.get("inputValue")
                if not param:
                        param = ""

                bar = ""
                if param:
                        lst = []
                        lst.append('safe')
                        lst.append(param)
                        lst.append('moresafe')
                        lst.pop(0)
                        bar = lst[0]

                import os
                import subprocess
                import helpers.utils

                argList = []
                if "Windows" in os.name:
                        argList.append("cmd.exe")
                        argList.append("-c")
                else:
                        argList.append("sh")
                        argList.append("-c")
                argList.append(f"echo {bar}")

                proc = subprocess.run(argList, capture_output=True, encoding="utf-8")
                RESPONSE += (
                        helpers.utils.commandOutput(proc)
                )

                return RESPONSE