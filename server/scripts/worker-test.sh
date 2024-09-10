#!/usr/bin/bash

# Takes a steam ID as a CLI argument

# Change to projects python directory
cd sbi-worker

# Run our python tests
~/v_envs/steamset/bin/python3 tests.py $1