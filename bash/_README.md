# IMPORTANT
These are sample bash scripts that can be used to help automate everything from setup -> testing. 

These scripts should ***ONLY*** be run from the root project directory. 

Example: 
```
./bash/setup.sh
./bash/start.sh
./bash/check.sh
./bash/test.sh
./bash/stop.sh
```

Here is a brief summary of what they all do:

/bash/setup.sh
 - This will create a .virtual_envs directory in the current users home folder
 - It will then change to that directory and create a new python virtual environment for the project
 - It will then activate the environment, update pip, and install all required python packges found in /python/flaskr/requirements.txt

/bash/start.sh
 - This will start celery and gunicorn/Flask in the background. Their logs can be found in /python/flaskr/logs

/bash/check.sh
 - This will check to see if there are any running gunicorn/celery processes

/bash/test.sh
 - This will call a simple tests.py file to enqueue a task and check its status

/bash/stop.sh
 - This will kill all celery / gunicorn processes. 
 
Do note 
 - In order to run /bash/start.sh or /bash/test.sh you will need to activate your python virtual environment first: ```source ~/.virtual_envs/steam_bi_dev/bin/activate```