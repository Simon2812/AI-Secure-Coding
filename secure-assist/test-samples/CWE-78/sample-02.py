from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route("/clone", methods=["POST"])
def clone_repo():
    url = request.form.get("repo_url")
    branch = request.form.get("branch", "main")
    cmd = f"git clone -b {branch} {url} /tmp/repo"
    proc = subprocess.run(cmd, shell=True, capture_output=True)
    return proc.stdout.decode()
