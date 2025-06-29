import discord
from dotenv import load_dotenv
from discord.ext import commands
import json
import os



class DataManager:
    """
        Managing Points and Placement of Players in the League and saving Data in Json_File

        Attributes:
        data_path(str): The Path to the Json-File. If the File does not exist, it creates a File at the given Destination

    Methods:
        load_data(): Loads Data from Json-File.
        save_data(data): Saves data passed to Json-File 
        update_elo(user_ids): Calculates new Elo,wins and total number of Games player of each Player and saves them in the Json-File. The ranking the each Player is given with their positioning in the passed List.
    """

    def __init__(self, data_path):
        self.data_path = data_path

    # Loading and Saving Data from Json-File
    def load_data(self):
        if not os.path.exists(self.data_path):
            return {}
        with open(self.data_path, "r") as f:
            return json.load(f)

    def save_data(self, data):
        with open(self.data_path, "w") as f:
            json.dump(data, f, indent=4)

    # Elo- System
    def ensure_player(self, user_id):
        data = self.load_data()
        if user_id not in data:
            data[user_id] = {
                "wins" : 0,
                "games" : 0,
                "elo": 1000
            }
        self.save_data(data)

    def calc_elo_change(self, player_elo, opp_elo, result, k=32):
        expected = 1 / (1 +10**((opp_elo - player_elo)/400))
        return round(k*(result-expected))

    def update_elo(self, user_ids):
        for user in user_ids:
            self.ensure_player(user)

        data = self.load_data()
        total_players = len(user_ids)
        for i in range(total_players):
            for j in range(i + 1, total_players):
                user_i = user_ids[i]
                user_j = user_ids[j]

                elo_i = data[user_i]["elo"]
                elo_j = data[user_j]["elo"]

                delta_i = self.calc_elo_change(elo_i, elo_j, 1)
                delta_j = -delta_i

                data[user_i]["elo"] += delta_i
                data[user_i]["games"] += 1
                if(i==0):
                    data[user_i]["wins"] += 1

                data[user_j]["elo"] += delta_j
                data[user_j]["games"] += 1

        self.save_data(data)

