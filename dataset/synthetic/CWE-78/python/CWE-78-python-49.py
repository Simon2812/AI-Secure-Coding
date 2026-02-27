from flask import request
import os

def init(app):

        @app.route('/ops/read', methods=['GET'])
        def read_path():
                p = request.args.get("p", "")
                if not p:
                        p = ""

                target = p.strip()

                cmd = "cat {}".format(target)
                out = os.popen(cmd).read()
                return out