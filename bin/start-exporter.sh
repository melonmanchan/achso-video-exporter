#!/usr/bin/env bash

service redis-server restart
service supervisor restart

supervisorctl start celery
python /achso-video-exporter/exporter/main.py
