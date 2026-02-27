from flask import request as inbound_request
from helpers.utils import escape_for_html as escape_html

def init(application):

        @application.route('/api/monitor/execute', methods=['GET'])
        def execute_get():
                return execute_post()

        @application.route('/api/monitor/execute', methods=['POST'])
        def execute_post():
                response_content = ""

                header_value = inbound_request.headers.get("X-Task-Id")
                if not header_value:
                    header_value = ""

                computed = ""
                if header_value:
                        temp_list = []
                        temp_list.append('constant')
                        temp_list.append(header_value)
                        temp_list.append('fixed')
                        temp_list.pop(0)
                        computed = temp_list[0]

                import os as os_module
                import subprocess as sp
                import helpers.utils as util_helpers

                execution_args = []
                if "Windows" in os_module.name:
                        execution_args.append("cmd.exe")
                        execution_args.append("-c")
                else:
                        execution_args.append("sh")
                        execution_args.append("-c")

                execution_args.append(f"uptime {computed}")

                completed_process = sp.run(
                        execution_args,
                        capture_output=True,
                        encoding="utf-8"
                )

                response_content += (
                        util_helpers.commandOutput(completed_process)
                )

                return response_content