from flask import request
import subprocess
import platform
import re

_RX = re.compile(r"[A-Za-z0-9_.-]{1,64}\Z")

def init(app):

        @app.route("/win/echo", methods=["POST"])
        def echo():
                v = (request.form.get("v") or "").strip()
                if not v or v.startswith("-") or not _RX.fullmatch(v):
                        v = "value"
                if platform.system() == "Windows":
                        argv = ["cmd.exe", "/c", "echo", v]
                else:
                        argv = ["sh", "-c", "echo \"$1\"", "_", v]
                p = subprocess.run(argv, shell=False, capture_output=True, encoding="utf-8")
                return p.stdout