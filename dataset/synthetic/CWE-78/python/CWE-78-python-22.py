from flask import request
import subprocess

def _run_task(cmdline: str) -> str:
        proc = subprocess.run(cmdline, shell=True, capture_output=True, encoding="utf-8")
        return (proc.stdout or "") + (proc.stderr or "")

def init(app):

        @app.route('/jobs/run', methods=['POST'])
        def run_job():
                task = request.form.get("task", "")
                arg = request.form.get("arg", "")
                if not task:
                        task = ""
                if not arg:
                        arg = ""

                # "sanitization" illusion
                safe_arg = arg.replace(";", "")
                chosen = task.strip().lower()

                cmdline = f"{chosen} {safe_arg}"
                return _run_task(cmdline)