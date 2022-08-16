from __future__ import print_function
from steam import SteamAPI
from steam_helper import SteamHelper
from datetime import datetime
from faker import Faker
import yaml
import mysql.connector


def main():
    with open('config.yaml', 'r') as cfg:
        config = yaml.safe_load(cfg)

    steam = config['steam']
    mysql_cfg = config['mysql']
    options = config['options']
    discover_friends = options['discover_friends']
    discover_games = options['discover_games']
    traverse_friends = options['traverse_friends']

    insert_game = ("""
        INSERT INTO game (app_id, name) VALUES (%(app_id)s, %(name)s)
        ON DUPLICATE KEY UPDATE name=%(name)s
    """)
    insert_gameinuse = ("""
        INSERT INTO gameinuse (playtime_forever_minutes, playtime_2weeks_minutes, user_fk, game_fk) VALUES (%(playtime_forever_minutes)s, %(playtime_2weeks_minutes)s, (SELECT user_pk FROM user WHERE steam_id=%(steam_id)s), (SELECT game_pk FROM game WHERE app_id=%(app_id)s))
        ON DUPLICATE KEY UPDATE playtime_forever_minutes=%(playtime_forever_minutes)s, playtime_2weeks_minutes=%(playtime_2weeks_minutes)s
    """)
    insert_user = ("""
        INSERT INTO user (steam_id, display_name) VALUES (%(steam_id)s, %(display_name)s)
        ON DUPLICATE KEY UPDATE display_name=%(display_name)s
    """)
    query_game = "SELECT app_id from game"

    steam_api = SteamAPI(key=steam['key'], debug=options['debug'])
    steam_ids = [steam['steamid']]

    view_friends = []
    view_gamesinuse = []

    if (discover_friends or traverse_friends):
        friend_list = steam_api.get_friend_list(
            steamId=steam['steamid'], include_player_summaries=False)
        if (friend_list):
            for friend in friend_list:
                steam_ids.append(friend['steamid'])
                friend.update({'user_fk': steam['steamid']})
            view_friends = friend_list

    if (traverse_friends):
        id_list = steam_ids.copy()
        for steam_id in id_list:
            if (discover_games):
                games = []
                games = steam_api.get_owned_games(
                    steam_id, include_store_data=False)
                if (games):
                    for game in games:
                        game.update({'steamid': steam_id})
                    view_gamesinuse.extend(games)
            if (discover_friends):
                friends = []
                friends = steam_api.get_friend_list(
                    steamId=steam_id, include_player_summaries=False)
                if (friends):
                    for friend in friends:
                        steam_ids.append(friend['steamid'])
                        friend.update({'user_fk': steam_id})
                    view_friends.extend(friends)

    else:
        if (discover_games):
            items = []
            items = steam_api.get_owned_games(
                steam_ids[0], include_store_data=False)
            if (items):
                for item in items:
                    item.update({'steamid': steam_ids[0]})
                view_gamesinuse.extend(items)
    
    steam_helper = SteamHelper(debug=options['debug'])
    guids = steam_helper.generate_guids(id_set=set(steam_ids))
    users = guids.copy()
    fake = Faker()
    for user in users:
        display_name = fake.word(part_of_speech='adjective').capitalize() + ' ' + fake.word(part_of_speech='noun').capitalize() + ' #' + str(fake.pyint())
        user.update({'display_name': display_name})
    assert len(set(user['display_name'] for user in users)) == len(users)

    if(options['destination'] == 'mysql'):
        cnx = mysql.connector.connect(host=mysql_cfg['host'], user=mysql_cfg['user'], password=mysql_cfg['password'], database=mysql_cfg['database'], connect_timeout=mysql_cfg['connect_timeout'])
        cursor = cnx.cursor(buffered=True, dictionary=True)

        # Query MySQL for a list of all app IDs
        print("%s\tQUERY\t%s" %(datetime.now(), query_game))
        cursor.execute(query_game)
        rows_game = cursor.fetchall()
        game_ids = [row['app_id'] for row in rows_game]

        for user in users:
            data_user = {
                'steam_id': user['steamid'],
                'display_name': user['display_name']
            }
            print("%s\tINSERT\t%s -> steam_bi[user]" %(datetime.now(), data_user))
            cursor.execute(insert_user, data_user)

        for game in view_gamesinuse:
            if (int(game['appid']) not in game_ids):
                game_ids.append(game['appid'])
                data_game = {
                    'app_id': game['appid'],
                    'name': game['name']
                }
                print("%s\tINSERT\t%s -> steam_bi[game]" %(datetime.now(), data_game))
                cursor.execute(insert_game, data_game)
            data_gameinuse = {
                'playtime_forever_minutes': game.get('playtime_forever', None),
                'playtime_2weeks_minutes': game.get('playtime_2weeks', None),
                'steam_id': game['steamid'],
                'app_id': game['appid']
            }
            print("%s\tINSERT\t%s -> steam_bi[gameinuse]" %(datetime.now(), data_gameinuse))
            cursor.execute(insert_gameinuse, data_gameinuse)
        cnx.commit()
        cursor.close()
        cnx.close()

    # Deprecated. Leaving for backwards compatability
    elif(options['destination'] == 'json'):
        for friend in view_friends:
            user_fk = friend['user_fk']
            friend.update({'user_fk': steam_helper.find_match(records=guids, key='steamid', value=user_fk)['guid']})
        
        steam_helper.replace_values(source_records=view_gamesinuse,target_records=guids, source_key='steamid', target_key='guid')
        steam_helper.replace_values(source_records=view_friends,target_records=guids, source_key='steamid', target_key='guid')
        steam_helper.write_data(data=guids, file_path='data/steam_bi_view_guids.json')
        steam_helper.write_data(data=view_gamesinuse,file_path='data/steam_bi_view_gamesinuse.json')
        steam_helper.write_data(data=view_friends,file_path='data/steam_bi_view_friends.json')

        for user in users:
            user.pop('steamid')
        steam_helper.write_data(data=users, file_path='data/steam_bi_view_users.json')

if __name__ == '__main__':
    main()
