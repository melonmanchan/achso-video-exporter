#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify
from utils import download_file, is_video_json_valid
from annotations import sort_annotations_by_time, is_annotation_json_valid
from videoeditor import bake_annotations

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    request_json = request.get_json()

    # Allow both plain JSON objects and arrays
    if type(request_json) is dict:
        request_json = [request_json]

    for video_json in request_json:
        if not is_video_json_valid(video_json) or not is_annotation_json_valid(video_json["annotations"]):
            return jsonify({"message": "Annotation json was malformed"}), 400
        else :
            video_uri = video_json["videoUri"]
            video_filename = video_uri.rsplit("/")[-1]
            video_location = download_file(video_uri, video_filename)
            sorted_annotations = sort_annotations_by_time(video_json["annotations"])
            bake_annotations(video_location, video_filename, sorted_annotations)

    return jsonify({"message": "Annotated video created succesfully"})

if __name__ == "__main__":
    app.run(debug=True)
