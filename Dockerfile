FROM dkarchmervue/python27-ffmpeg

RUN add-apt-repository ppa:chris-lea/redis-server
RUN apt-get update
RUN apt-get install -y ghostscript imagemagick redis-server
RUN mkdir /achso-video-exporter
ADD . /achso-video-exporter
WORKDIR /achso-video-exporter
RUN /usr/local/bin/pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "/achso-video-exporter/exporter/main.py"]
