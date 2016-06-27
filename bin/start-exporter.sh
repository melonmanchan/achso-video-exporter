#!/usr/bin/env bash

supervisorctl start celery
python /achso-video/exporter/main.py
