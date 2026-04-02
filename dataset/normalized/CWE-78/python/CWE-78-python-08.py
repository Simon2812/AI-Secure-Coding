from flask import request as inbound
from helpers.utils import escape_for_html as escape_html

def init(application):

        @application.route('/internal/queue/process-432', methods=['GET'])
        def process_432_get():
                return process_432_post()

        @application.route('/internal/queue/process-432', methods=['POST'])
        def process_432_post():
                response_body = ""

                selected_key = ""
                for field_name in inbound.form.keys():
                        if "process-432" in inbound.form.getlist(field_name):
                                selected_key = field_name
                                break

                import base64 as b64
                encoded = b64.b64encode(selected_key.encode('utf-8'))
                decoded_value = b64.b64decode(encoded).decode('utf-8')

                import platform as sys_platform
                import subprocess as sp_module
                import helpers.utils as util_mod

                shell_command = ""
                if sys_platform.system() == "Windows":
                        shell_command = "cmd.exe /c "
                else:
                        shell_command = "sh -c "

                shell_command += f"hostname {decoded_value}"

                try:
                        completed_proc = sp_module.run(
                                shell_command,
                                shell=True,
                                capture_output=True,
                                encoding="utf-8"
                        )

                        response_body += util_mod.commandOutput(completed_proc)

                except IOError:
                        response_body += "Execution failure"

                return response_body