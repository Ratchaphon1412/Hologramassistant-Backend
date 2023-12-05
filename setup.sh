#!/bin/bash
poetry run python3 manage.py collectstatic --noinput
poetry run python3 manage.py makemigrations 
poetry run python3 manage.py migrate  --noinput
poetry run gunicorn --bind 0.0.0.0:8024 HologramassistantBackend.wsgi 