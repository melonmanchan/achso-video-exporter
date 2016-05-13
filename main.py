#!/usr/bin/env python3

from flask import Flask
from flask import request
from utils import download_file

app = Flask(__name__)

@app.route("/", methods=["POST"])
def hello():
    content = request.get_json()
    video_uri = content["videoUri"]
    download_file(video_uri, video_uri.rsplit("/")[-1])
    return video_uri

if __name__ == "__main__":
    app.run(debug=True)
