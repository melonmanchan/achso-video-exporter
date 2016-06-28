# AchSo! video exporter
## Description
This is a RESTful service made in Python 2.7.10 and Flask/MoviePy to bake annotations into AchSo!-videos

The basic operation of this service goes like this:

1. A JSON payload is send, containing one or more video annotation manifests and an email
2. The payload is validated in main.py
3. A response is sent, indicating that the request was in an acceptable format
4. Meanwhile, a seperate task is started to bake the annotations and pauses into the videos
5. After the video files are done, they are zipped up and uploaded to Amazon S3 bucket, where they can be accessed
6. Finally, a download link is sent to the email address in question

## Running

Intended deployment is to be done within Docker. First, clone this repository.

```
git clone https://github.com/melonmanchan/achso-video-exporter
```

Then, copy the config.py file in the exporter subfolder into a file called local_config.py, and add your environment
variables (port, AWS S3 credentials, sendgrid credentials).

```python
S3_SECRET_KEY = 'SECRET HERE'
S3_ACCESS_KEY = 'ACCESS KEY HERE'
SENDGRID_API_KEY = 'SENDGRID API KEY HERE'
```

then, simply cd into the cloned repository and build the image

```sh
cd achso-video-exporter
docker build -t exporter .
```

and run it!

```sh
docker run --name exporter -p 5000:5000 exporter
```

## Example payload

```json
{
    "email": "testi.tyyppi@aalto.fi",
    "videos": [{
        "annotations": [
            {
                "author": {
                    "id": "",
                    "name": "Testi Tyyppi",
                    "uri": ""
                },
                "createdTimestamp": "2016-05-16T16:11:46.344+03:00",
                "position": {
                    "x": 0.4719,
                    "y": 0.61824
                },
                "text": "box",
                "time": 4727
            },
            {
                "author": {
                    "id": "",
                    "name": "Testi Tyyppi",
                    "uri": ""
                },
                "createdTimestamp": "2016-05-16T16:12:09.049+03:00",
                "position": {
                    "x": 0.64708,
                    "y": 0.59025
                },
                "text": "bk",
                "time": 1560
            },
            {
                "author": {
                    "id": "",
                    "name": "Testi Tyyppi",
                    "uri": ""
                },
                "createdTimestamp": "2016-05-16T16:12:37.585+03:00",
                "position": {
                    "x": 0.42274,
                    "y": 0.59508
                },
                "text": "key",
                "time": 6264
            }
        ],
        "author": {
            "id": "",
            "name": "Testi Tyyppi",
            "uri": ""
        },
        "date": "2016-05-16T16:11:25.076+03:00",
        "deleteUri": "https://layersbox.aalto.fi/govitra/uploads/video-123456",
        "editedBy": "Testi Tyyppi",
        "formatVersion": 1,
        "genre": "good_work",
        "id": "1234-45687-923",
        "location": {
            "accuracy": 28.826,
            "latitude": 60.1782634,
            "longitude": 24.828596
        },
        "revision": 1,
        "rotation": 0,
        "thumbUri": "https://aalto-achso.s3.eu-central-1.amazonaws.com/thumbs/video-1234-45687-923.jpg",
        "title": "Example video payload",
        "uploadedAt": "2016-05-16T13:13:21Z",
        "videoUri": "https://aalto-achso.s3.eu-central-1.amazonaws.com/videos/video-1234-45687-923.mp4"
    }]
}

```

