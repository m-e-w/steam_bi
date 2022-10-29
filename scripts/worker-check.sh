#!/usr/bin/bash

# Check for gunicorn processes
printf "[gunicorn]\n"
ps auxww | grep '/.virtual_envs/steam_bi_dev/bin/python3' | grep 'gunicorn' | grep -v ' grep '

# Check for celery processes
printf "[celery]\n"
ps auxww | grep '/.virtual_envs/steam_bi_dev/bin/python3' | grep 'celery' | grep -v ' grep '
