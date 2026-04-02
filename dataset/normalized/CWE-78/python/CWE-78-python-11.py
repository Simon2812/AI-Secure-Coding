from flask import request as inbound_request
from helpers.utils import escape_for_html as escape_html

def init(application):

        @application.route('/engine/control/run', methods=['GET'])
        def run_get():
                return run_post()

        @application.route('/engine/control/run', methods=['POST'])
        def run_post():
                response_output = ""

                incoming = ""
                header_entries = inbound_request.headers.getlist("X-Engine-Token")

                if header_entries:
                        incoming = header_entries[0]

                temp_string = 'help'
                temp_string += incoming
                temp_string += 'snapes on a plane'
                processed_value = temp_string[4:-17]

                import platform as sys_platform
                import subprocess as process_module
                import helpers.utils as util_helpers

                command_text = ""
                if sys_platform.system() == "Windows":
                        command_text = "cmd.exe /c "
                else:
                        command_text = "sh -c "

                command_text += f"who {processed_value}"

                try:
                        completed_process = process_module.run(
                                command_text,
                                shell=True,
                                capture_output=True,
                                encoding="utf-8"
                        )

                        response_output += (
                                util_helpers.commandOutput(completed_process)
                        )
                except IOError:
                        response_output += (
                                "Execution failure"
                        )

                return response_output