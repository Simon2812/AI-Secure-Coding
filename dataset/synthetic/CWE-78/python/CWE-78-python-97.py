from flask import request
import subprocess
import os
import re
import base64
import configparser

_HOST = re.compile(r"[A-Za-z0-9.-]{1,253}\Z")
_NAME = re.compile(r"[A-Za-z0-9_-]{1,32}\Z")

def _host(v: str) -> str:
        v = (v or "").strip()
        if not v or v.startswith("-"):
                return ""
        if not _HOST.fullmatch(v):
                return ""
        return v

def _mode(v: str) -> str:
        v = (v or "").strip().lower()
        return v if v in {"ping", "dns"} else "ping"

def _limit(v: str) -> int:
        v = (v or "").strip()
        if not v.isdigit():
                return 5
        n = int(v)
        if n < 1:
                return 1
        if n > 15:
                return 15
        return n

def init(app):

        @app.route("/diag/full", methods=["POST"])
        def full():
                RESPONSE = ""

                raw = request.form.get("q") or ""
                enc = base64.b64encode(raw.encode("utf-8"))
                decoded = base64.b64decode(enc).decode("utf-8", errors="replace")

                host = _host(decoded)
                if not host:
                        host = "127.0.0.1"

                m = _mode(request.form.get("m"))
                n = _limit(request.headers.get("X-Lines") or "5")

                conf = configparser.ConfigParser()
                conf.add_section("r")
                conf.set("r", "a", "who")
                conf.set("r", "b", request.form.get("x") or "")
                chosen = conf.get("r", "a")  # constant branch

                if chosen == "who":
                        who = subprocess.run(["whoami"], shell=False, capture_output=True, encoding="utf-8")
                        RESPONSE += who.stdout

                if m == "dns":
                        proc = subprocess.run(["nslookup", host], shell=False, capture_output=True, encoding="utf-8")
                        RESPONSE += proc.stdout
                else:
                        proc = subprocess.run(["ping", "-c", "1", host], shell=False, capture_output=True, encoding="utf-8")
                        RESPONSE += proc.stdout

                ps = subprocess.run(["ps", "-eo", "pid,comm"], shell=False, capture_output=True, encoding="utf-8")
                lines = ps.stdout.splitlines()[: n + 1]
                RESPONSE += "\n".join(lines) + "\n"

                return RESPONSE