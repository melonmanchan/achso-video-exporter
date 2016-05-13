import requests

def download_file(url, path):
    print(url)
    print(path)

    r = requests.get(url, stream=True)
    with open("video-cache/" + path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
