import nba_scraper.nba_scraper as ns
#import nba_parser as npar
import pandas as pd
from pymongo import MongoClient
from twoplayer import runTwoPlayer
from playertotals import PlayerTotals
import os.path
import json
import pdmongo as pdm
client = MongoClient('localhost', 27017)

ortg_dict = {
}

from collections import defaultdict

# Initialize dictionary


with open('player_keys/2016-17.json') as json_file:
    playerDict = json.load(json_file)

year = 2017

def loadJson():
    ortg_dict = defaultdict(list)

    game_ids = list(range(int(f"2{year - 2001}00001"), int(f"2{year - 2001}01231")))
    collection_ids = list(filter(lambda x: x % 10 == 0, game_ids))

    pbp_objects = []
    i = 0
    for collection_id in collection_ids:
        print(collection_id)
        df = pdm.read_mongo(str(collection_id), [], f"mongodb://localhost:27017/{year - 1}-{year % 2000}")
        pbp_objects.append(df)

    rapm_possession = pd.concat([x for x in pbp_objects])

    for index, row in rapm_possession.iterrows():
        for i in range(5):
            ortg_dict[row[f"off_player_{i + 1}_id"]].append(row[f"points_made"])

    with open(f"player_keys/{year - 1}-{year % 2000}_ORTG.json", 'w') as f:
        json.dump(ortg_dict, f)


def getOrtg():
    with open(f'player_keys/{year - 1}-{year % 2000}_ORTGpossessions.json') as json_file:
        ortg_dict = json.load(json_file)

    player_ortg = {
    }

    for key in ortg_dict:
        sum = 0
        for elem in ortg_dict[key]:
            sum+=elem
        sum/= (len(ortg_dict[key])/100)
        player_ortg[key] = round(sum, 2)

    with open(f"player_keys/{year - 1}-{year % 2000}_playerOrtg.json", 'w') as f:
        json.dump(player_ortg, f)

def getTeammateOrtg():
    teammate_ortg_dict_list = defaultdict(list)
    teammate_ortg_dict = defaultdict(float)

    with open(f'player_keys/{year - 1}-{year % 2000}_playerOrtg.json') as json_file:
        player_ortg = json.load(json_file)

    game_ids = list(range(int(f"2{year - 2001}00001"), int(f"2{year - 2001}01231")))
    collection_ids = list(filter(lambda x: x % 10 == 0, game_ids))

    pbp_objects = []
    for collection_id in collection_ids:
        print(collection_id)
        df = pdm.read_mongo(str(collection_id), [], f"mongodb://localhost:27017/{year - 1}-{year % 2000}")
        pbp_objects.append(df)

    rapm_possession = pd.concat([x for x in pbp_objects])

    def calcNum(row, index):
        sum = 0
        for j in range(5):
            sum += player_ortg[str(row[f"off_player_{j + 1}_id"])]

        sum -= player_ortg[str(row[f"off_player_{index + 1}_id"])] #subtract self
        return sum/4


    for index, row in rapm_possession.iterrows():
        for i in range(5):
            teammate_ortg_dict_list[row[f"off_player_{i + 1}_id"]].append(calcNum(row, i))

    print("done")

    for key in teammate_ortg_dict_list:
        sum = 0
        for elem in teammate_ortg_dict_list[key]:
            sum+=elem
        sum/= (len(teammate_ortg_dict_list[key]))
        teammate_ortg_dict[key] = round(sum, 2)

    with open(f"player_keys/{year - 1}-{year % 2000}_teammate_Ortg.json", 'w') as f:
        json.dump(teammate_ortg_dict, f)



getTeammateOrtg()

