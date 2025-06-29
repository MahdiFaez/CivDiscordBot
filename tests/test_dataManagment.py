import pytest
import os
from utils.dataManagment import DataManager

dm = DataManager("tests/testing_ranking.json")
dm.save_data({})

@pytest.mark.parametrize("user_ids, expected", [
    (["Phil", "Mahdi"], {
        "Phil" : {
            "wins" : 1,
            "games" : 1,
            "elo": 1016
        },
        "Mahdi" :{
            "wins" : 0,
            "games" : 1,
            "elo": 984
        },
    }),
    (["Phil", "Mahdi"], {
        "Phil" : {
            "wins" : 2,
            "games" : 2,
            "elo": 1031
        },
        "Mahdi" :{
            "wins" : 0,
            "games" : 2,
            "elo": 969
        },
    }),
    (["Mahdi", "Tom", "Phil"], {
        "Phil" : {
            "wins" : 2,
            "games" : 3,
            "elo": 1031-19-17
        },
        "Mahdi" :{
            "wins" : 1,
            "games" : 3,
            "elo": 969+17+19
        },
        "Tom" :{
            "wins" : 0,
            "games" : 1,
            "elo": 1000-17+17
        },
    }),
])
def test_update_elo(user_ids, expected):
    dm.update_elo(user_ids)
    assert dm.load_data() == expected