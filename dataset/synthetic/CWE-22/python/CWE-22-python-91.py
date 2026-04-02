import os
from flask import Flask, request, send_file, abort

app = Flask(__name__)

media_store = "/opt/media/videos"


@app.route("/video", methods=["GET"])
def video():
    vid = request.args.get("id", "").strip()

    available = os.listdir(media_store)
    if vid not in available:
        abort(404)

    path = os.path.join(media_store, vid)
    return send_file(path)