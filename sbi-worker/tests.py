import requests
import json
import time
import sys

# Takes a steam ID as a CLI argument
steam_id = sys.argv[1]

# Send a post request to enqueue a task
data = {"steamid":steam_id, "discover_games": True, "discover_friends": False, "traverse_friends": True}
headers = {"Content-Type": "application/json"}
r = requests.post(url="http://127.0.0.1:8000/api/1.0/task/steam/", json=data, headers=headers)
print(r.status_code)
print(json.dumps(r.json(), indent=2))

if(r.status_code == 200):
    pass
else:
    exit()

# Make a few get calls to check the status of the task.
number_of_gets = 5
time_to_sleep = 3
for i in range(number_of_gets):
    time.sleep(time_to_sleep)
    task_id = r.json().get('task_id')
    r = requests.get(url="http://127.0.0.1:8000/api/1.0/task/steam/" + task_id)
    print(r.status_code)
    print(json.dumps(r.json(), indent=2))