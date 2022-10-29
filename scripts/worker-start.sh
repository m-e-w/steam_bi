#!/usr/bin/bash

# Change to the worker directory
cd sbi-worker

# Start celery in the background
~/.virtual_envs/steam_bi_dev/bin/celery -A tasks worker --loglevel=DEBUG --logfile logs/celery.log --detach

# Start gunicorn in the background
~/.virtual_envs/steam_bi_dev/bin/gunicorn -w 1 'wsgi:app' --log-level DEBUG --log-file logs/gunicorn.log --daemon