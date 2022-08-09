from steam import SteamAPI
from steam_helper import SteamHelper
import yaml


def main():
    with open('config.yaml', 'r') as cfg:
        config = yaml.safe_load(cfg)

    steam = config['steam']
    options = config['options']
    steam_ids = [steam['steamid']]
    root_games = []
    root_friends = []
    steam_api = SteamAPI(key=steam['key'], debug=options['debug'])

    if(steam['data']['get_games']):
        root_games = steam_api.get_owned_games(steamId=steam['steamid'], include_store_data=False, store_limit=10, time_to_sleep=2)

    if(steam['data']['get_friends']):
        root_friends = steam_api.get_friend_list(steamId=steam['steamid'], include_player_summaries=False)
        for friend in root_friends:
            steam_ids.append(friend['steamid'])

    if(steam['data']['traverse_friends']):
        for friend in root_friends:
            games = steam_api.get_owned_games(steamId=friend['steamid'], include_store_data=False, store_limit=10, time_to_sleep=2)
            friends = steam_api.get_friend_list(steamId=friend['steamid'], include_player_summaries=False)
            friend['games'] = games
            friend['friends'] = friends
            for f in friends:
                steam_ids.append(f['steamid'])

    steam_helper = SteamHelper(debug=options['debug'], counter=steam_api.get_counter())
    
    guids = steam_helper.generate_guids(id_set=set(steam_ids))
    root_guid = steam_helper.find_match(records=guids, key='steamid', value=steam['steamid'])['guid']
    steam_helper.replace_values(source_records=root_friends, target_records=guids, source_key='steamid', target_key='guid', sub_list_key='friends')

    player = {
        'steamid': root_guid,
        'games': root_games,
        'friends': root_friends
    }
    data = {
        'player': player,
    }

    steam_helper.write_data(data=data, file_path='data/steam_bi_data_extract.json')
    steam_helper.write_data(data=guids, file_path='data/steam_bi_steamid_guid.json')


if __name__ == '__main__':
    main()
