from flask import request
import subprocess

def _fmt(template: str, value: str) -> str:
        return template.format(value=value)

def init(app):

        @app.route('/img/convert', methods=['POST'])
        def convert():
                mode = request.form.get("mode", "")
                src = request.form.get("src", "")
                if not mode:
                        mode = ""
                if not src:
                        src = ""

                op = mode.strip().lower()
                path = src.strip()

                template = "convert {value} out.png"
                if op == "resize":
                        template = "convert {value} -resize 50% out.png"

                cmd = _fmt(template, path)
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")
                return proc.stdout + proc.stderr