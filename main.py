#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify
from utils import download_file, sort_annotations_by_time
from videoeditor import bake_annotations

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    content = request.get_json()
    video_uri = content["videoUri"]
    video_filename = video_uri.rsplit("/")[-1]

    video_location = download_file(video_uri, video_filename)
    sorted_annotations = sort_annotations_by_time(content["annotations"])
    bake_annotations(video_location, video_filename, sorted_annotations)

    return jsonify({"message": "Annotated video created succesfully"})

if __name__ == "__main__":
    app.run(debug=True)
