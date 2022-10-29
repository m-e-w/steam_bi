#!/usr/bin/bash

# Stop gunicorn
ps auxww | grep '/.virtual_envs/steam_bi_dev/bin/python3' | grep 'gunicorn' | grep -v ' grep ' | awk '{print $2}' | xargs kill -9

# Stop celery
ps auxww | grep '/.virtual_envs/steam_bi_dev/bin/python3' | grep 'celery' | grep -v ' grep ' | awk '{print $2}' | xargs kill -9
