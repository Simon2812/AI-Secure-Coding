from flask import request
from helpers.utils import escape_for_html

def init(app):

        @app.route('/tools/system/tool', methods=['GET'])
        def mail_get():
                return mail_post()

        @app.route('/tools/system/tool', methods=['POST'])
        def mail_post():
                RESPONSE = ""

                param = request.form.get("inputValue")
                if not param:
                        param = ""

                TestParam = "This should never happen"
                if 'should' not in TestParam:
                        bar = "Ifnot case passed"
                else:
                        bar = param

                import platform
                import subprocess
                import helpers.utils

                argument = ""
                if platform.system() == "Windows":
                        argument = "cmd.exe /c "
                else:
                        argument = "sh -c "
                argument += f"echo {bar}"

                try:
                        proc = subprocess.run(argument, shell=True, capture_output=True, encoding="utf-8")

                        RESPONSE += (
                                helpers.utils.commandOutput(proc)
                        )
                except IOError:
                        RESPONSE += (
                                "Problem executing command"
                        )

                return RESPONSE