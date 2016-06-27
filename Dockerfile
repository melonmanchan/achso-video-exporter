FROM dkarchmervue/python27-ffmpeg
RUN apt-get update
RUN apt-get install -y software-properties-common

RUN add-apt-repository ppa:chris-lea/redis-server
RUN apt-get update
RUN apt-get install -y ghostscript imagemagick redis-server
RUN pip install supervisor

RUN mkdir /achso-video-exporter
ADD . /achso-video-exporter
WORKDIR /achso-video-exporter

ENV IMAGEIO_FFMPEG_EXER /usr/local/bin/ffmpeg

RUN /usr/local/bin/pip install -r requirements.txt
RUN cp celery.conf /etc/supervisor/conf.d/celery.conf

EXPOSE 5000

CMD ["bash", "/achso-video-exporter/bin/start-exporter.sh"]
