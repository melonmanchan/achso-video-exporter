FROM python:3.4

RUN apt-get update
RUN apt-get install -y ghostscript imagemagick libav-tools
RUN mkdir /achso-video-exporter
ADD . /achso-video-exporter
WORKDIR /achso-video-exporter
RUN cp ./policy.xml /etc/ImageMagick-6/policy.xml
RUN /usr/local/bin/pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python", "/achso-video-exporter/main.py"]
