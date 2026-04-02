from flask import redirect, url_for, request, make_response, render_template
from helpers.utils import escape_for_html

def init(app):

        @app.route('/service/inspect', methods=['GET'])
        def inspect_get():
                return inspect_post()

        @app.route('/service/inspect', methods=['POST'])
        def inspect_post():
                RESPONSE = ""

                import helpers.separate_request

                wrapper = helpers.separate_request.request_wrapper(request)
                query_input = wrapper.get_query_parameter("inspect")
                if not query_input:
                        query_input = ""

                import configparser

                result_token = 'safe!'
                configuration = configparser.ConfigParser()
                configuration.add_section('runtime_section')
                configuration.set('runtime_section', 'primary_key', 'a_Value')
                configuration.set('runtime_section', 'secondary_key', query_input)

                result_token = configuration.get('runtime_section', 'primary_key')

                import platform
                import subprocess
                import helpers.utils

                command_string = ""
                if platform.system() == "Windows":
                        command_string = "cmd.exe /c "
                else:
                        command_string = "sh -c "
                command_string += f"echo {result_token}"

                try:
                        proc = subprocess.run(command_string, shell=True, capture_output=True, encoding="utf-8")

                        RESPONSE += (
                                helpers.utils.commandOutput(proc)
                        )
                except IOError:
                        RESPONSE += (
                                "Problem executing subprocess"
                        )

                return RESPONSE