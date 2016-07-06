import os
import re
import requests
import shutil
import tempfile
import dateutil.parser


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
    return zip_endpoint + '.zip'


def is_video_json_valid(json_payload):
    if not json_payload["videoUri"] or not json_payload["title"]:
        return False
    return True


def parse_iso_date(date):
    if date is None:
        return "an unknown time"

    parsed = dateutil.parser.parse(date)

    return parsed.strftime("%Y.%m.%d %H:%M:%S")


def newlinify_string(string, insert_newline_at):
    lines = []
    lines_inserted = 0
    for i in xrange(0, len(string), insert_newline_at):
        lines_inserted += 1
        lines.append(string[i:i + insert_newline_at])

    return '\n'.join(lines), lines_inserted

