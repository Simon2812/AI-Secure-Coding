from flask import Flask, request
import shutil

app = Flask(__name__)
UPLOAD_DIR = "/data/uploads"
ARCHIVE_DIR = "/data/archive"

@app.route("/archive", methods=["POST"])
def archive_file():
    src = request.form.get("source")
    dst = request.form.get("destination")
    src_path = f"{UPLOAD_DIR}/{src}"
    dst_path = f"{ARCHIVE_DIR}/{dst}"
    shutil.move(src_path, dst_path)
    return "archived"
