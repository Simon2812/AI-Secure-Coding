from flask import request
import subprocess
import re

_WORD = re.compile(r"[A-Za-z0-9_-]{1,24}\Z")

def _needle(v: str) -> str:
        v = (v or "").strip()
        if not v or not _WORD.fullmatch(v):
                return "root"
        return v

def _cap(v: str) -> int:
        v = (v or "").strip()
        if not v.isdigit():
                return 10
        n = int(v)
        if n < 1:
                return 1
        if n > 40:
                return 40
        return n

def init(app):

        @app.route("/proc/filter", methods=["POST"])
        def filter():
                RESPONSE = ""

                q = _needle(request.form.get("q"))
                limit = _cap(request.headers.get("X-Limit") or "10")

                base = subprocess.run(
                        ["ps", "-eo", "user,comm,%cpu,%mem", "--sort=-%cpu"],
                        shell=False,
                        capture_output=True,
                        encoding="utf-8"
                )

                data = base.stdout
                if not data:
                        return RESPONSE

                g = subprocess.run(
                        ["grep", q],
                        shell=False,
                        input=data,
                        capture_output=True,
                        encoding="utf-8"
                )

                out_lines = (g.stdout or "").splitlines()
                RESPONSE += "\n".join(out_lines[:limit]) + "\n"

                wc = subprocess.run(
                        ["wc", "-l"],
                        shell=False,
                        input=g.stdout,
                        capture_output=True,
                        encoding="utf-8"
                )

                RESPONSE += "count=" + (wc.stdout or "").strip() + "\n"
                return RESPONSE
