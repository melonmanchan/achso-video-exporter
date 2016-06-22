FROM dkarchmervue/python27-ffmpeg

RUN apt-get update
RUN apt-get install -y ghostscript imagemagick
RUN mkdir /achso-video-exporter
ADD . /achso-video-exporter
WORKDIR /achso-video-exporter
RUN /usr/local/bin/pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "/achso-video-exporter/exporter/main.py"]
