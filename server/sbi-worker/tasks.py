from celery import Celery
from faker import Faker
from steam import SteamAPI
from datetime import datetime
from env import *
from sql import *
import logging
import mysql.connector

steam = SteamAPI(key=steam_key)
fake = Faker()
# filename='steam_bi.log', filemode='w', removing. This is no longer needed as celery/gunicorn logs will be used instead
if(debug):
    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.ERROR, format='%(name)s - %(levelname)s - %(message)s')


def fetch_steam_friends(steamId, include_player_summaries, steam_ids):
    friends = []
    friends = steam.get_friend_list(steamId=steamId, include_player_summaries=include_player_summaries)
    if (friends):
        for friend in friends:
            steam_ids.append(friend['steamid'])
            friend.update({'user_fk': steamId})
    return friends

def fetch_steam_games(steam_id, include_store_data):
    games = []
    games = steam.get_owned_games(steam_id, include_store_data=False)
    if (games):
        for game in games:
            game.update({'steamid': steam_id})
    return games

def get_steam_users(steam_ids):
    users = []
    for steam_id in steam_ids:
        display_name = fake.word(part_of_speech='adjective').capitalize() + ' ' + fake.word(part_of_speech='noun').capitalize() + ' #' + str(fake.pyint())
        user = {
            'steamid': steam_id,
            'display_name': display_name
        }
        users.append(user)
    return users

app = Celery('tasks', backend='redis://' + redis_host + ':6379', broker='pyamqp://guest@' + rabbitmq_host + '//')

@app.task
def task_steam(steamid, discover_friends, discover_games, traverse_friends):
    steam_ids = [steamid]
    user_records = []
    friend_records = []
    gameinuse_records = []

    print("Attempting to validate Steam ID: %s" % (steamid))
    players = steam.get_player_summaries(steamids=steamid)

    if(players):
        print("Steam ID: Valid. Progressing")
    else:
        error_message = "Failed to validate Steam ID"
        print(error_message)
        return {'msg': error_message}

    print("Gathering data from steam ...)")

    if (discover_friends or traverse_friends):
        friends = fetch_steam_friends(steamId=steamid, include_player_summaries=False, steam_ids=steam_ids)
        if (friends):
            friend_records.extend(friends)

    if (discover_games):
        games = fetch_steam_games(steam_id=steamid, include_store_data=False)
        if (games):
            gameinuse_records.extend(games)

    if (traverse_friends):
        id_list = steam_ids.copy()
        # Remove the root users steam id
        id_list.pop(0)
        for steam_id in id_list:
            if (discover_games):
                games = fetch_steam_games(steam_id=steam_id, include_store_data=False)
                if (games):
                    gameinuse_records.extend(games)
            if (discover_friends):
                friends = fetch_steam_friends(steamId=steam_id, include_player_summaries=False, steam_ids=steam_ids)
                if (friends):
                    friend_records.extend(friends)
    
    users = get_steam_users(steam_ids=steam_ids)
    if (users):
        user_records.extend(users)

    cnx = mysql.connector.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database, connect_timeout=mysql_connect_timeout)
    cursor = cnx.cursor(buffered=True, dictionary=True)

    print("%s\tGathering data from MySQL ..." %(datetime.now()))
    # Query MySQL for a list of all app IDs
    if(debug):
        logging.debug("%s\tQUERY\t%s" %(datetime.now(), query_game))
    cursor.execute(query_game)
    rows_game = cursor.fetchall()
    game_ids = [row['app_id'] for row in rows_game]
    count_game = len(game_ids)

    print("%s\tWriting data to MySQL ..." %(datetime.now()))
    for user in user_records:
        data_user = {
            'steam_id': user['steamid'],
            'display_name': user['display_name']
        }
        if(debug):
            logging.debug("INSERT\t%s -> steam_bi[user]" %(data_user))
        cursor.execute(insert_user, data_user)

    for game in gameinuse_records:
        if (int(game['appid']) not in game_ids):
            game_ids.append(game['appid'])
            data_game = {
                'app_id': game['appid'],
                'name': game['name']
            }
            if(debug):
                logging.debug("INSERT\t%s -> steam_bi[game]" %(data_game))
            cursor.execute(insert_game, data_game)
        data_gameinuse = {
            'playtime_forever_minutes': game.get('playtime_forever', None),
            'playtime_2weeks_minutes': game.get('playtime_2weeks', None),
            'steam_id': game['steamid'],
            'app_id': game['appid']
        }
        if(debug):
            logging.debug("INSERT\t%s -> steam_bi[gameinuse]" %(data_gameinuse))
        cursor.execute(insert_gameinuse, data_gameinuse)
    cnx.commit()
    cursor.close()
    cnx.close()

    response_dict = {"user": len(user_records), "game": len(game_ids) - count_game, "gameinuse": len(gameinuse_records)}
    return response_dict