#!/usr/bin/bash

steam_bi_dir=$PWD

mkdir ~/.virtual_envs
cd ~/.virtual_envs

python3 -m venv steam_bi_dev
source steam_bi_dev/bin/activate
pip install --upgrade pip

pip install -r "$steam_bi_dir/python/flaskr/requirements.txt"


