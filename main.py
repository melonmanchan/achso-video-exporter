#!/usr/bin/env python3

from flask import Flask
from flask import request
from flask import jsonify
from utils import download_file, create_temp_dir, zip_up_dir, delete_dir
from annotations import sort_annotations_by_time
from videoeditor import bake_annotations

app = Flask(__name__)


@app.route("/", methods=["POST"])
def index():
    request_json = request.get_json()

    # Allow both plain JSON objects and arrays
    if type(request_json) is dict:
        request_json = [request_json]


    for video_json in request_json:
        export_dir_name = create_temp_dir()

        video_uri = video_json["videoUri"]
        video_filename = video_uri.rsplit("/")[-1]
        video_location = download_file(video_uri, "video-cache/" + video_filename)
        sorted_annotations = sort_annotations_by_time(video_json["annotations"])
        bake_annotations(video_location, export_dir_name + '/' + video_filename, sorted_annotations)

        zip_up_dir(export_dir_name, 'video-exports/' + video_json["title"])
        delete_dir(export_dir_name)


    return jsonify({"message": "Annotated video created succesfully"})

if __name__ == "__main__":
    app.run(debug=True)
