from flask import request
import os
import subprocess
import re

_RX = re.compile(r"[A-Za-z0-9_.-]{1,64}\Z")

def init(app):

        @app.route("/text/out", methods=["GET"])
        def out():
                v = (os.environ.get("APP_LABEL") or "").strip()
                if not v or v.startswith("-") or not _RX.fullmatch(v):
                        v = "label"

                proc = subprocess.run(["sh", "-c", "printf '%s\n' \"$1\"", "_", v],
                                   shell=False, capture_output=True, encoding="utf-8")
                return proc.stdout