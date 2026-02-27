from flask import request
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9_.-]{1,64}\Z")

def init(app):

        @app.route("/text/out1", methods=["POST"])
        def out1():
                s = (request.form.get("t") or "").strip()
                if not s or s.startswith("-") or not _RX.fullmatch(s):
                        s = "value"
                proc = subprocess.run(["sh", "-c", "printf '%s\n' \"$1\"", "_", s],
                                   shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout