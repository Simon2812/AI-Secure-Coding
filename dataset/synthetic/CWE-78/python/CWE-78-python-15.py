from flask import request
import os
import subprocess
import helpers.utils

def init(app):

        @app.route('/files/archive', methods=['POST'])
        def archive_file():
                RESPONSE = ""

                filename = request.form.get("file", "")
                fmt = request.form.get("fmt", "")
                if not filename:
                        filename = ""
                if not fmt:
                        fmt = ""

                # keep logic simple; user controls format -> injected into command
                base = filename.strip()
                kind = fmt.strip().lower()

                cmd_line = f"tar -c{kind}f {base}.tar.{kind} {base}"
                p = subprocess.run(cmd_line, shell=True, capture_output=True, encoding="utf-8")

                RESPONSE += helpers.utils.commandOutput(p)
                return RESPONSE