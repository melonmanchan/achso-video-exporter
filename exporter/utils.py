import os
import requests
import shutil
import tempfile


def download_file(url, end_point):
    """Downloads a file by streaming using the requests module"""
    r = requests.get(url, stream=True)
    with open(end_point, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return end_point


def create_temp_dir():
    return tempfile.mkdtemp(suffix='video-exports-')


def delete_file(file_to_delete):
    os.remove(file_to_delete)


def delete_dir(dir_to_delete):
    shutil.rmtree(dir_to_delete)


def zip_up_dir(folder_to_zip, zip_endpoint):
    shutil.make_archive(zip_endpoint, 'zip', folder_to_zip)


def is_video_json_valid(json_payload):
    if not json_payload["videoUri"] or not json_payload["title"]:
        return False
    return True
