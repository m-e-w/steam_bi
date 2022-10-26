#!/usr/bin/bash

# Change to projects python directory
cd python/flaskr/

# Start celery in the background
celery -A tasks worker --loglevel=DEBUG --logfile logs/celery.log --detach

# Start gunicorn in the background
gunicorn -w 1 'wsgi:app' --log-level DEBUG --log-file logs/gunicorn.log --daemon