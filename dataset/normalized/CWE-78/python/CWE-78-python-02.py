from flask import request
from helpers.utils import escape_for_html

def init(app):

        @app.route('/tools/system/execute-166', methods=['GET'])
        def execute_166_get():
                return execute_166_post()

        @app.route('/tools/system/execute-166', methods=['POST'])
        def execute_166_post():
                RESPONSE = ""

                param = request.form.get("inputValue")
                if not param:
                        param = ""

                data_map = {}
                data_map['keyA'] = 'a-Value'
                data_map['keyB'] = param
                data_map['keyC'] = 'another-Value'
                bar = data_map['keyB']

                import platform
                import subprocess
                import helpers.utils

                arg = ""
                if platform.system() == "Windows":
                        arg = "cmd.exe /c "
                else:
                        arg = "sh -c "
                arg += f"echo {bar}"

                try:
                        proc = subprocess.run(arg, shell=True, capture_output=True, encoding="utf-8")

                        RESPONSE += (
                                helpers.utils.commandOutput(proc)
                        )
                except IOError:
                        RESPONSE += (
                                "Problem executing command"
                        )

                return RESPONSE