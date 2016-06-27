#!/usr/bin/env bash

service supervisor stop
service supervisor start

supervisorctl start celery
python /achso-video-exporter/exporter/main.py
