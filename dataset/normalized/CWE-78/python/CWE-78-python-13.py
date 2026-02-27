from flask import request as inbound_request
from helpers.utils import escape_for_html as html_escape

def init(application):

        @application.route('/core/agent/execute-1191', methods=['GET'])
        def execute_1191_get():
                return execute_1191_post()

        @application.route('/core/agent/execute-1191', methods=['POST'])
        def execute_1191_post():
                response_buffer = ""

                import helpers.separate_request as request_adapter

                wrapped_request = request_adapter.request_wrapper(inbound_request)
                input_value = wrapped_request.get_form_parameter("jobToken")
                if not input_value:
                        input_value = ""

                import os as os_module
                import subprocess as sp_module
                import helpers.utils as util_helpers

                execution_chain = []
                if "Windows" in os_module.name:
                        execution_chain.append("cmd.exe")
                        execution_chain.append("-c")
                else:
                        execution_chain.append("sh")
                        execution_chain.append("-c")

                execution_chain.append(f"groups {input_value}")

                completed_process = sp_module.run(
                        execution_chain,
                        capture_output=True,
                        encoding="utf-8"
                )

                response_buffer += (
                        util_helpers.commandOutput(completed_process)
                )

                return response_buffer