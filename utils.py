import requests


def download_file(url, end_point):
    r = requests.get(url, stream=True)
    with open("video-cache/" + end_point, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return "video-cache" + end_point
