from datetime import datetime
import uuid
import os
import json


class SteamHelper:
    """
    Class to hold a few helper functions to work with the data returned from Steams API

    :param str counter: Operations counter for logging
    """
    def __init__(self, debug: bool, counter: int):
        self.debug = debug
        self.counter = counter

    def find_match(self, records: list[dict], key: str, value: str):
        """
        Search a list of dictionaries by key:value. Return the matching dictionary

        :param list[dict] records: Records to search
        :param str key: Key to search for
        :param str value: Value to match on
        """
        return next(record for record in records if record[key] == value)

    def generate_guids(self, id_set: list):
        """
        Takes a set of steamids and generates a guid per each item. Returns a list of dictionaries containing the original steamid and the new guid

        :param list[dict] id_set: A set of steamids
        """
        items = []
        for id in id_set:
            item = {
                'guid': uuid.uuid4().hex,
                'steamid': id
            }
            items.append(item)
        return items

    def replace_values(self, source_records: list[dict], target_records: list[dict], source_key: str, target_key: str, **kwargs):
        """
        Replaces all values of source_key within source_records with the value of target_key from target_records

        :param list[dict] source_records: The source records whose key will be replaced
        :param list[dict] target_records: The target records that are matched to
        :param str source_key: The key whose value is to be replaced
        :param str target_key: The key containing the value to use
        :param str sub_list_key: (Optional) If source_records contains another list to replace records in, specify it here
        """
        sub_list_key = kwargs.get('sub_list_key', None)
        for record in source_records:
            match = self.find_match(records=target_records, key=source_key, value=record[source_key])
            record[source_key] = match[target_key]

            items = record.get(sub_list_key, [])
            for item in items:
                match = self.find_match(records=target_records, key=source_key, value=item[source_key])
                item[source_key] = match[target_key]

    def write_data(self, file_path: str, data: list[dict]):
        """
        Takes a list of dictionaries and writes it to a json file

        :param str file_path: The path to write the file
        :param list[dict] data: The list of dictionaries to be write to disk
        """
        self.counter = self.counter + 1
        if(file_path):
            if(self.debug):
                print("[%s]\t%s\tWRITE\t%s" % (self.counter, datetime.now(), os.path.abspath(file_path)))

            with open(file_path, 'w') as f:
                json.dump(data, f)
