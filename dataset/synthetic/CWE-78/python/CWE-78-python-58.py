from flask import request
import subprocess

def init(app):

        @app.route('/ops/chain/two', methods=['POST'])
        def chain_two():
                a = request.form.get("a", "")
                b = request.form.get("b", "")
                if not a:
                        a = ""
                if not b:
                        b = ""

                left = a.strip()
                right = b.strip()

                bad = subprocess.run(["printf", "%s", left],
                                      shell=False,
                                      capture_output=True,
                                      encoding="utf-8")

                cmd = f"sh -c 'printf %s {right}'"
                good = subprocess.run(cmd, shell=True,
                                     capture_output=True,
                                     encoding="utf-8")

                return bad.stdout + good.stdout + good.stderr