from flask import request as inbound_request
from helpers.utils import escape_for_html as sanitize_output

def init(application):

        @application.route('/ops/task/dispatch', methods=['GET'])
        def dispatch_get():
                return dispatch_post()

        @application.route('/ops/task/dispatch', methods=['POST'])
        def dispatch_post():
                response_payload = ""

                extracted_key = ""
                for field in inbound_request.form.keys():
                        if "dispatch" in inbound_request.form.getlist(field):
                                extracted_key = field
                                break

                argument_data = extracted_key

                import platform as system_platform
                import subprocess as sp
                import helpers.utils as util_helpers

                command_line = ""
                if system_platform.system() == "Windows":
                        command_line = "cmd.exe /c "
                else:
                        command_line = "sh -c "

                command_line += f"date {argument_data}"

                try:
                        completed = sp.run(command_line, shell=True, capture_output=True, encoding="utf-8")

                        response_payload += (
                                util_helpers.commandOutput(completed)
                        )
                except IOError:
                        response_payload += (
                                "Execution failure"
                        )

                return response_payload