from datetime import datetime
import uuid
import os
import json


# Class to hold a few helper functions to work with the data returned from Steams API
class SteamHelper:
    def __init__(self, debug: bool, counter: int):
        self.debug = debug
        self.counter = counter

    # Search a list of dictionaries by key:value. Return the matching dictionary.
    def find_match(self, records: list[dict], key: str, value: str):
        return next(record for record in records if record[key] == value)

    # Takes a set of steamids and generates a guid per each item. Returns a list of dictionaries containing the original steamid and the new guid
    def generate_guids(self, id_set: list):
        items = []
        for id in id_set:
            item = {
                'guid': uuid.uuid4().hex,
                'steamid': id
            }
            items.append(item)
        return items

    # Replaces all values of source_key within source_records with the value of target_key from target_records
    def replace_values(self, source_records: list[dict], target_records: list[dict], source_key: str, target_key: str):
        for record in source_records:
            match = self.find_match(
                records=target_records, key=source_key, value=record[source_key])
            record[source_key] = match[target_key]
            for friend in record['friends']:
                match = self.find_match(
                    records=target_records, key=source_key, value=friend[source_key])
                friend['steamid'] = match[target_key]

    # Takes a list of dictionaries and writes it to a json file
    def write_data(self, file_path: str, data: list[dict]):
        self.counter = self.counter + 1
        if(file_path):
            if(self.debug):
                print("[%s]\t%s\tWRITE\t%s" % (self.counter,
                      datetime.now(), os.path.abspath(file_path)))

            with open(file_path, 'w') as f:
                json.dump(data, f)
