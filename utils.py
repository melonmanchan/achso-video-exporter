import requests


def download_file(url, end_point):
    """Downloads a file by streaming using the requests module"""
    r = requests.get(url, stream=True)
    with open("video-cache/" + end_point, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return "video-cache/" + end_point

def sort_annotations_by_time(annotations):
    return sorted(annotations, key=lambda k: k["time"])
