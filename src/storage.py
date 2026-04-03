import json


class DataManager():
    def __init__(self, filepath: str):
        self.filepath = filepath

    def save_post(self, clean_post: dict):
        try:
            with open(self.filepath, 'r') as fil:
                data_list = json.load(fil)
        except (FileNotFoundError, json.JSONDecodeError):
            data_list = []
        data_list.append(clean_post)
        with open(self.filepath, 'w') as fil:
            json.dump(data_list, fil, indent=4)
