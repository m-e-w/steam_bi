from steam import SteamAPI
from steam_helper import SteamHelper
from faker import Faker
import yaml


def main():
    with open('config.yaml', 'r') as cfg:
        config = yaml.safe_load(cfg)

    # Config data
    steam = config['steam']
    options = config['options']
    discover_friends = options['discover_friends']
    discover_games = options['discover_games']
    traverse_friends = options['traverse_friends']

    steam_api = SteamAPI(key=steam['key'], debug=options['debug'])
    steam_ids = [steam['steamid']]

    view_friends = []
    view_gamesinuse = []

    if (discover_friends or traverse_friends):
        friend_list = steam_api.get_friend_list(steamId=steam['steamid'], include_player_summaries=False)
        if (friend_list):
            for friend in friend_list:
                steam_ids.append(friend['steamid'])
            view_friends = friend_list

    if (traverse_friends):
        id_list = steam_ids.copy()
        for steam_id in id_list:
            if (discover_games):
                items = []
                items = steam_api.get_owned_games(steam_id, include_store_data=False)
                if (items):
                    for item in items:
                        item.update({'steamid': steam_id})
                    view_gamesinuse.extend(items)
            # if(discover_friends):
            #     items = []
            #     items = steam_api.get_friend_list(steamId=steam_id, include_player_summaries=False)
            #     if(items):
            #         for item in items:
            #             steam_ids.append(item['steamid'])
            #             item.update({'friend_of': steam_id})
            #         view_friends.extend(items)
                
    else:
        if (discover_games):
            items = []
            items = steam_api.get_owned_games(steam_ids[0], include_store_data=False)
            if (items):
                for item in items:
                    item.update({'steamid': steam_ids[0]})
                view_gamesinuse.extend(items)

    steam_helper = SteamHelper(debug=options['debug'], counter=steam_api.get_counter())
    guids = steam_helper.generate_guids(id_set=set(steam_ids))

    steam_helper.replace_values(source_records=view_friends,target_records=guids, source_key='steamid', target_key='guid')
    steam_helper.replace_values(source_records=view_gamesinuse,target_records=guids, source_key='steamid', target_key='guid')

    steam_helper.write_data(data=guids, file_path='data/steam_bi_view_guids.json')
    steam_helper.write_data(data=view_gamesinuse,file_path='data/steam_bi_view_gamesinuse.json')

    users = guids.copy()
    fake = Faker()
    for user in users:
        display_name = fake.word(part_of_speech='adjective').capitalize() + ' ' + fake.word(part_of_speech='noun').capitalize() + ' #' + str(fake.pyint())
        user.update({'display_name': display_name})
        user.pop('steamid')
    steam_helper.write_data(data=users, file_path='data/steam_bi_view_users.json')

    # Check to see if display names are unique, throw an error if not
    assert len(set(user['display_name'] for user in users)) == len(users)


if __name__ == '__main__':
    main()
