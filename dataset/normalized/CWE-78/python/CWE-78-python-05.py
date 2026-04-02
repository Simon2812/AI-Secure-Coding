from flask import request
from helpers.utils import escape_for_html

def init(app):

        @app.route('/admin/system/run', methods=['GET'])
        def run_get():
                return run_post()

        @app.route('/admin/system/run', methods=['POST'])
        def run_post():
                RESPONSE = ""

                entries = request.form.getlist("userInput")
                selected = ""
                if entries:
                        selected = entries[0]

                container = {}
                container['alpha'] = 'fixed'
                container['beta'] = selected
                container['gamma'] = 'static'
                bar = container['beta']

                import os
                import subprocess
                import helpers.utils

                command_parts = []
                if "Windows" in os.name:
                        command_parts.append("cmd.exe")
                        command_parts.append("-c")
                else:
                        command_parts.append("sh")
                        command_parts.append("-c")

                command_parts.append(f"whoami {bar}")

                proc = subprocess.run(command_parts, capture_output=True, encoding="utf-8")
                resp += (
                        helpers.utils.commandOutput(proc)
                )

                return resp