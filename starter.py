from steam import SteamAPI
from steam_helper import SteamHelper
import yaml


def main():
    with open('config.yaml', 'r') as cfg:
        config = yaml.safe_load(cfg)

    # Config data
    steam = config['steam']
    options = config['options']

    steam_api = SteamAPI(key=steam['key'], debug=options['debug'])
    steam_ids = [steam['steamid']]

    view_friends = []
    friend_list = steam_api.get_friend_list(steamId=steam['steamid'], include_player_summaries=False)
    if(friend_list):
        for friend in friend_list:
            steam_ids.append(friend['steamid'])
        view_friends = friend_list

    view_gamesinuse = []
    for steam_id in steam_ids:
        items = []
        items = steam_api.get_owned_games(steam_id, include_store_data=False)
        if(items):
            for item in items:
                item.update({'steamid': steam_id})
            view_gamesinuse.extend(items)

    steam_helper = SteamHelper(debug=options['debug'], counter=steam_api.get_counter())
    guids = steam_helper.generate_guids(id_set=set(steam_ids))

    steam_helper.replace_values(source_records=view_friends, target_records=guids, source_key='steamid', target_key='guid')
    steam_helper.replace_values(source_records=view_gamesinuse, target_records=guids, source_key='steamid', target_key='guid')

    steam_helper.write_data(data=view_friends, file_path='data/steam_bi_view_friends.json')
    steam_helper.write_data(data=view_gamesinuse, file_path='data/steam_bi_view_gamesinuse.json')
    steam_helper.write_data(data=guids, file_path='data/steam_bi_view_guids.json')


if __name__ == '__main__':
    main()
