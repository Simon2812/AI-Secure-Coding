from flask import request as inbound_request
from helpers.utils import escape_for_html as html_escape

def init(application):

        @application.route('/service/api/process-899', methods=['GET'])
        def process_899_get():
                return process_899_post()

        @application.route('/service/api/process-899', methods=['POST'])
        def process_899_post():
                response_data = ""

                import helpers.separate_request as req_wrapper

                wrapped_request = req_wrapper.request_wrapper(inbound_request)
                input_value = wrapped_request.get_query_parameter("taskId")
                if not input_value:
                        input_value = ""

                selector = "ABC"
                current = selector[0]

                match current:
                        case 'A':
                                argument_value = input_value
                        case 'B':
                                argument_value = 'bob'
                        case 'C' | 'D':
                                argument_value = input_value
                        case _:
                                argument_value = "bob's your uncle"

                import os as os_module
                import subprocess as sp
                import helpers.utils as util_helpers

                execution_list = []
                if "Windows" in os_module.name:
                        execution_list.append("cmd.exe")
                        execution_list.append("-c")
                else:
                        execution_list.append("sh")
                        execution_list.append("-c")

                execution_list.append(f"users {argument_value}")

                completed = sp.run(
                        execution_list,
                        capture_output=True,
                        encoding="utf-8"
                )

                response_data += (
                        util_helpers.commandOutput(completed)
                )

                return response_data