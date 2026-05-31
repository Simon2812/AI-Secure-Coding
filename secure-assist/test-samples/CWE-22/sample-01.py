from flask import Flask, request, send_file

app = Flask(__name__)
BASE = "/var/www/uploads"

@app.route("/download")
def download():
    filename = request.args.get("file", "")
    path = BASE + "/" + filename
    return send_file(path)
