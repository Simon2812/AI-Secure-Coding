from flask import request
import subprocess
import os

def init(app):

        @app.route('/repo/git', methods=['POST'])
        def git_status():
                repo = request.form.get("repo", "")
                if not repo:
                        repo = ""

                base = repo.strip()

                cmd = "git status --porcelain"
                p = subprocess.run(cmd, shell=True, cwd=base, capture_output=True, encoding="utf-8")

                return p.stdout + p.stderr