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
