from flask import request
import subprocess

def init(app):

        @app.route('/ops/service/control', methods=['POST'])
        def control_service():
                service = request.form.get("service", "")
                action = request.form.get("action", "")
                if not service:
                        service = ""
                if not action:
                        action = ""

                svc = service.strip()
                act = action.strip()

                cmd = f"systemctl {act} {svc}"
                proc = subprocess.run(cmd, shell=True, capture_output=True, encoding="utf-8")

                return (proc.stdout or "") + (proc.stderr or "")