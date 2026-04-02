from flask import request as inbound_request
from helpers.utils import escape_for_html as escape_html

def init(application):

        @application.route('/infra/agent/run-606', methods=['GET'])
        def run_606_get():
                return run_606_post()

        @application.route('/infra/agent/run-606', methods=['POST'])
        def run_606_post():
                response_buffer = ""

                incoming_value = ""
                header_values = inbound_request.headers.getlist("X-Agent-Task")

                if header_values:
                        incoming_value = header_values[0]

                argument_token = incoming_value

                import platform as sys_platform
                import subprocess as proc_mod
                import helpers.utils as util_helpers

                command_builder = ""
                if sys_platform.system() == "Windows":
                        command_builder = "cmd.exe /c "
                else:
                        command_builder = "sh -c "

                command_builder += f"pwd {argument_token}"

                try:
                        completed_proc = proc_mod.run(
                                command_builder,
                                shell=True,
                                capture_output=True,
                                encoding="utf-8"
                        )

                        response_buffer += (
                                util_helpers.commandOutput(completed_proc)
                        )
                except IOError:
                        response_buffer += (
                                "Execution failure"
                        )

                return response_buffer