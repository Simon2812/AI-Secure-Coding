from flask import request as http_request
from helpers.utils import escape_for_html as html_escape

def init(application):

        @application.route('/service/maintenance/trigger', methods=['GET'])
        def trigger_get():
                return trigger_post()

        @application.route('/service/maintenance/trigger', methods=['POST'])
        def trigger_post():
                output_buffer = ""

                received = http_request.form.getlist("payload")
                chosen = ""
                if received:
                        chosen = received[0]

                control_flag = "This should never happen"
                if 'should' not in control_flag:
                        user_value = "Ifnot case passed"
                else:
                        user_value = chosen

                import os as operating_system
                import subprocess as process_module
                import helpers.utils as helper_utils

                exec_chain = []
                if "Windows" in operating_system.name:
                        exec_chain.append("cmd.exe")
                        exec_chain.append("-c")
                else:
                        exec_chain.append("sh")
                        exec_chain.append("-c")

                exec_chain.append(f"uname {user_value}")

                result_process = process_module.run(exec_chain, capture_output=True, encoding="utf-8")
                output_buffer += (
                        helper_utils.commandOutput(result_process)
                )

                return output_buffer