import requests


def download_file(url, end_point):
    """Downloads a file by streaming using the requests module"""
    r = requests.get(url, stream=True)
    with open("video-cache/" + end_point, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return "video-cache/" + end_point


def is_video_json_valid(json_payload):
    if not json_payload["videoUri"] or not json_payload["title"]:
        return False
    return True
