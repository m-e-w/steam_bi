#!/usr/bin/bash

# Check for gunicorn processes
ps auxww | grep '/.virtual_envs/steam_bi_dev/bin/python3' | grep 'gunicorn' | grep -v ' grep '

# Check for celery processes
ps auxww | grep '/.virtual_envs/steam_bi_dev/bin/python3' | grep 'celery' | grep -v ' grep '