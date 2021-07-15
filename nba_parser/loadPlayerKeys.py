import nba_scraper.nba_scraper as ns
import nba_parser as npar
import pandas as pd
import numpy as np
from pymongo import MongoClient
import json
client = MongoClient('localhost', 27017)

import pdmongo as pdm

playerkey_dict = {
}

from collections import defaultdict

# Initialize dictionary
twoPlayer_dict = defaultdict(int)

print(client.list_database_names())


def updateTwoPlayerCounter(names, ids):
    id = str(ids[0]) + "-" + str(ids[1])
    id1 = str(ids[0]) + "-" + str(ids[2])
    id2 = str(ids[0]) + "-" + str(ids[3])
    id3 = str(ids[0]) + "-" + str(ids[4])

    twoPlayer_dict[id] += 1
    twoPlayer_dict[id1] += 1
    twoPlayer_dict[id2] += 1
    twoPlayer_dict[id3] += 1

    id1 = str(ids[1]) + "-" + str(ids[2])
    id2 = str(ids[1]) + "-" + str(ids[3])
    id3 = str(ids[1]) + "-" + str(ids[4])

    twoPlayer_dict[id1] += 1
    twoPlayer_dict[id2] += 1
    twoPlayer_dict[id3] += 1

    id2 = str(ids[2]) + "-" + str(ids[3])
    id3 = str(ids[2]) + "-" + str(ids[4])

    twoPlayer_dict[id2] += 1
    twoPlayer_dict[id3] += 1

    id3 = str(ids[3]) + "-" + str(ids[4])
    twoPlayer_dict[id3] += 1



year = 2018
game_ids = list(range(int(f"2{year - 2001}00001"), int(f"2{year - 2001}01231")))
collection_ids = list(filter(lambda x: x % 10 == 0, game_ids))
for collection_id in collection_ids:
    df = pdm.read_mongo(str(collection_id), [], "mongodb://localhost:27017/2017-18")
    for index, row in df.iterrows():
        names = [row['def_player_1'], row['def_player_2'], row['def_player_3'], row['def_player_4'],row['def_player_5'], row['off_player_1'], row['off_player_2'], row['off_player_3'], row['off_player_4'],row['off_player_5']]
        ids = [row['def_player_1_id'], row['def_player_2_id'],row['def_player_3_id'],row['def_player_4_id'],row['def_player_5_id'], row['off_player_1_id'],row['off_player_2_id'],row['off_player_3_id'],row['off_player_4_id'],row['off_player_5_id']]
        updateTwoPlayerCounter(names[:5], np.sort(ids[:5]))
        updateTwoPlayerCounter(names[-5:], np.sort(ids[-5:]))
        for i in range(10):
            playerkey_dict.update({names[i]: [(ids[i])]})

with open(f"player_keys/{year - 1}-{year%2000}.json", 'w') as f:
    json.dump(playerkey_dict, f)

with open(f"player_keys/{year - 1}-{year%2000}_pair_count.json", 'w') as f:
    json.dump(twoPlayer_dict, f)