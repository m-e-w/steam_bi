#!/usr/bin/bash

# Takes a steam ID as a CLI argument

# Change to projects python directory
cd sbi-worker

# Run our python tests
~/.virtual_envs/steam_bi_dev/bin/python3 tests.py $1