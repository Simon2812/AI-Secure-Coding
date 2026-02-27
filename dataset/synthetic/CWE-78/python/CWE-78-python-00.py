from flask import request
import subprocess
import os
import re

_REPO = re.compile(r"[A-Za-z0-9_-]{1,64}\Z")

def _repo_name(v: str) -> str:
        v = (v or "").strip()
        if not v or not _REPO.fullmatch(v):
                return ""
        return v

def _repo_dir(name: str) -> str:
        base = os.path.abspath("/srv/projects")
        path = os.path.abspath(os.path.join(base, name))
        if not (path == base or path.startswith(base + os.sep)):
                return ""
        if not os.path.isdir(path):
                return ""
        if not os.path.isdir(os.path.join(path, ".git")):
                return ""
        return path

def _op(v: str) -> str:
        v = (v or "").strip().lower()
        return v if v in {"branch", "status", "log"} else "status"

def init(app):

        @app.route("/repo/util", methods=["POST"])
        def util():
                RESPONSE = ""

                name = _repo_name(request.form.get("p"))
                if not name:
                        return RESPONSE

                cwd = _repo_dir(name)
                if not cwd:
                        return RESPONSE

                op = _op(request.form.get("op"))

                table = {
                        "branch": ["git", "branch"],
                        "status": ["git", "status", "--porcelain"],
                        "log": ["git", "log", "-n", "3", "--oneline"],
                }
                argv = table[op]

                p = subprocess.Popen(argv, cwd=cwd, shell=False,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out, err = p.communicate()

                if out:
                        RESPONSE += out
                if err:
                        RESPONSE += err

                return RESPONSE