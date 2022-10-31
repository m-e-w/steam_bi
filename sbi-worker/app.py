#from celery.result import AsyncResult
from flask import Flask, request, jsonify, Response
from tasks import task_steam

app = Flask(__name__)

@app.route('/api/1.0/task/steam/<task_id>', methods=['GET'])
def get_steam_task_status(task_id):
    task_result = task_steam.AsyncResult(task_id=task_id)
    result = {
        'task_id': task_result.task_id,
        'task_status': task_result.status,
        'task_result': task_result.result
    }
    return jsonify(result)

@app.route('/api/1.0/task/steam/', methods=['POST'])
def create_steam_task():
    data = request.json
    steamid = data.get('steamid')

    if(steamid.isnumeric() and len(steamid) == 17):
        pass
    else:
        return jsonify({"Error": "Non 64 Bit Steam ID Supplied"}), 422
    
    discover_friends = data.get('discover_friends')
    discover_games = data.get('discover_games')
    traverse_friends = data.get('traverse_friends')

    task_result = task_steam.delay(steamid=steamid, discover_friends=discover_friends, discover_games=discover_games, traverse_friends=traverse_friends)
    result = {
        'task_id': task_result.task_id,
        'task_status': task_result.status,
        'task_result': task_result.result
    }
    return jsonify(result)
