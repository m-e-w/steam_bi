from steam import SteamAPI
from steam_helper import SteamHelper
import yaml


def main():
    # Open the config file
    with open('config.yaml', 'r') as cfg:
        config = yaml.safe_load(cfg)

    # Get config data
    steam = config['steam']
    options = config['options']

    steam_api = SteamAPI(key=steam['key'], debug=options['debug'])

    # Get games and friends of the root user
    my_games = steam_api.get_owned_games(
        steamId=steam['steamid'], include_store_data=False, store_limit=10, time_to_sleep=2)
    my_friends = steam_api.get_friend_list(
        steamId=steam['steamid'], include_player_summaries=False)

    # List to hold all steamids (We will later take all steamids, de-dupe them, and generate a guid per each steamid to facilitate data anonymization)
    steam_ids = []

    # Add the root users steamid to our list of ids
    steam_ids.append(steam['steamid'])

    # Loop through each friend and grab their games and friends
    for friend in my_friends:
        # Add the friends steamid to our list of ids
        steam_ids.append(friend['steamid'])
        games = steam_api.get_owned_games(
            steamId=friend['steamid'], include_store_data=False, store_limit=10, time_to_sleep=2)
        friends = steam_api.get_friend_list(
            steamId=friend['steamid'], include_player_summaries=False)

        # Loop through all of their friends and add their friends ids to the list
        for f in friends:
            steam_ids.append(f['steamid'])

        # Save their games / friends
        friend['games'] = games
        friend['friends'] = friends

    steam_helper = SteamHelper(
        debug=options['debug'], counter=steam_api.get_counter())

    # Pass the de-duped list of steamids, and retrieve a list of dicts containing the steamid/guid
    guids = steam_helper.generate_guids(id_set=set(steam_ids))

    # Replace all steamids with a guid
    steam_helper.replace_values(
        source_records=my_friends, target_records=guids, source_key='steamid', target_key='guid')

    # Look for our own matching guid
    match = steam_helper.find_match(
        records=guids, key='steamid', value=steam['steamid'])

    # Build the dataset
    player = {
        'steamid': match['guid'],
        'games': my_games,
        'friends': my_friends
    }
    data = {
        'player': player,
    }

    # Write the dataset and the list of guids/steamids (We save this so we can un-anonymize the data later on if we want)
    steam_helper.write_data(
        data=data, file_path='data/steam_bi_data_extract.json')
    steam_helper.write_data(
        data=guids, file_path='data/steam_bi_steamid_guid.json')


if __name__ == '__main__':
    main()
