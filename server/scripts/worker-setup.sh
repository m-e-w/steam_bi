#!/usr/bin/bash

# Get the current working directory
steam_bi_dir=$PWD

# Make a directory for our python virtual environments
mkdir ~/.virtual_envs

# Create the python virtual environment for our worker
cd ~/.virtual_envs
python3 -m venv steam_bi_dev

# Active the workers virtual environment and upgrade pip
source steam_bi_dev/bin/activate
pip install --upgrade pip

# Install the required python packages for our worker
pip install -r "$steam_bi_dir/sbi-worker/requirements.txt"


