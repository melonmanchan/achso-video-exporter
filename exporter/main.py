#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify

import uuid

from utils import download_file, create_temp_dir, zip_up_dir, delete_dir, is_video_json_valid, delete_file
from annotations import sort_annotations_by_time, is_annotation_json_valid
from s3 import upload_file

from videoeditor import bake_annotations

import config

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    request_json = request.get_json()

    # Allow both plain JSON objects and arrays
    if type(request_json) is dict:
        request_json = [request_json]

    export_dir_name = create_temp_dir()
    for video_json in request_json:
        if not is_video_json_valid(video_json):
            return jsonify({"message": "A video json was malformed"}), 400
        if not video_json["annotations"]:
            # TODO: Handle video with no annotations
            break
        if not is_annotation_json_valid(video_json["annotations"]):
            return jsonify({"message": "An annotation json was malformed"}), 400
        else:
            video_uri = video_json["videoUri"]
            video_filename = video_uri.rsplit("/")[-1]
            video_location = download_file(video_uri, "../video-cache/" + video_filename)
            sorted_annotations = sort_annotations_by_time(video_json["annotations"])
            bake_annotations(video_location, export_dir_name + "/" + video_json["title"] + ".mp4", sorted_annotations)
            delete_file("../video-cache/" + video_filename)

    export_zip_name = '../video-exports/AchSo-Video-Export-' + str(uuid.uuid4())
    export_zip_name = zip_up_dir(export_dir_name, export_zip_name)
    delete_dir(export_dir_name)
    upload_file(export_zip_name)
    return jsonify({"message": "Annotated video created successfully"})

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
