from datetime import datetime
import requests
import time


# Class to perform Steam API requests
class SteamAPI:
    def __init__(self, key, debug):
        self.key = key
        self.output_format = 'json'
        self.debug = debug
        self.request_counter = 0

    # Return the count of requests made
    def get_counter(self):
        return self.request_counter

    # Private method to send a GET request and return the response in JSON format
    def __getter(self, url: str, params: dict) -> dict:
        self.request_counter = self.request_counter + 1
        response_dict = {}
        if(self.debug):
            print("[%s]\t%s\tGET\t%s" %
                  (self.request_counter, datetime.now(), url))

        response = requests.get(url=url, params=params)

        if(response.status_code == 200):
            response_dict = response.json()

        return response_dict

    # Takes a appid and returns data from the store
    def __get_app_details(self, appid: int) -> dict:
        item = {}
        url = 'https://store.steampowered.com/api/appdetails'
        params = {
            'appids': str(appid)
        }
        item = self.__getter(url=url, params=params).get(
            str(appid)).get('data')

        return item

    # Takes a comma separated list of steamids and returns basic properties about the player(s)
    def get_player_summaries(self, steamids: str) -> list[dict]:
        items = []
        url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
        params = {
            'key': self.key,
            'steamids': steamids,
            'format': self.output_format
        }
        items = self.__getter(url=url, params=params).get(
            'response').get('players')

        return items

    # Takes a steamid and returns the users list of owned games. ** (Optional): Iclude additional game store data **
    def get_owned_games(self, steamId: str, include_store_data: bool, store_limit: int, time_to_sleep: int):
        items = []
        url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
        params = {
            'key': self.key,
            'steamid': steamId,
            'format': self.output_format,
            'include_appinfo': True,
            'include_played_free_games': True
        }
        items = self.__getter(url=url, params=params).get(
            'response').get('games')

        if(include_store_data):
            counter = 0
            for item in items:
                if(counter < store_limit):
                    counter = counter + 1
                    item.update(
                        {'app_details': self.__get_app_details(appid=item['appid'])})
                    time.sleep(time_to_sleep)

        return items

    # Takes a steamid and returns the users list of friends. ** (Optional): Include additional player profile data **
    def get_friend_list(self, steamId: str, include_player_summaries: bool) -> list[dict]:
        items = []
        url = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
        params = {
            'key': self.key,
            'steamid': steamId,
            'format': self.output_format,
            'relationship:': 'all'
        }
        response = self.__getter(url=url, params=params)

        if(response):
            items = response.get('friendslist').get('friends')

        if(items and include_player_summaries):
            steamid_list = [item['steamid'] for item in items]
            steamids = ",".join(str(steamid) for steamid in steamid_list)

            records = self.__get_player_summaries(steamids=steamids)

            for record in records:
                item = next(item for item in items if item.get(
                    'steamid') == record.get('steamid'))

                friend_since = item.get('friend_since')
                if(friend_since):
                    item.update({'friend_since': str(
                        datetime.utcfromtimestamp(int(friend_since)))})

                timecreated = record.get('timecreated')
                if(timecreated):
                    record.update(
                        {'timecreated': str(datetime.utcfromtimestamp(int(timecreated)))})

                lastlogoff = record.get('lastlogoff')
                if(lastlogoff):
                    record.update(
                        {'lastlogoff': str(datetime.utcfromtimestamp(int(lastlogoff)))})

                item.update({'player': record})

        return items
