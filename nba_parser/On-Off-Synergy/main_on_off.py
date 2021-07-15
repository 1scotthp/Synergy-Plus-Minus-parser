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

year1 = 2017
year2 = 2018
minPossessions = 2000


twoPlayer_path_sample1 = f"player_keys/{year1 - 1}-{year1 % 2000}_pair_count.json"
twoPlayer_path_sample2 = f"player_keys/{year2 - 1}-{year2 %2000}_pair_count.json"

with open('player_keys/2016-17.json') as json_file:
    playerDict = json.load(json_file)

with open(twoPlayer_path_sample1) as json_file2:
    twoPlayer_dict_sample1 = json.load(json_file2)

with open(twoPlayer_path_sample2) as json_file3:
    twoPlayer_dict_sample2 = json.load(json_file3)


def get_key(val):
    for key, value in playerDict.items():
        if [val] == value:
            return key


master_filename = f"2-player-rapms-{year2 - 1}-{year2%2000}/2-player-master.csv"
#gets altered possession matrix
def twoPlayerRapm(name1, name2, year):
    [id1] = playerDict[name1]
    [id2] = playerDict[name2]
    id = float(str(id1) + str(id2))

    possessions = runTwoPlayer(id1, id2, year)

    #gets rapm values
    player_rapm_df = PlayerTotals.player_rapm_results(possessions)
    df = player_rapm_df.sort_values(by='rapm', ascending=False)
    df.to_csv(f"2-player-rapms-{year - 1}-{year%2000}/" + name1 + "-" + name2 + "_rapm.csv")

    pairRapm = df.loc[df['player_id'] == id]
    print("RAPM:")
    print(pairRapm)

    if not os.path.isfile(master_filename):
        pairRapm.to_csv(master_filename)
    else:
        master = pd.read_csv(master_filename, index_col=0)
        master = master.append(pairRapm)
        master.to_csv(master_filename)

def callPlayerPairs(names, year):
    for pair in names:
        print("next")
        p1 = int(pair.split('-')[0])
        p2 = int(pair.split('-')[1])
        id = int(str(p1) + str(p2))
        if os.path.isfile(master_filename):
            master = pd.read_csv(master_filename)
            if id not in master.values:
                twoPlayerRapm(get_key(p1), get_key(p2), year)
        else:
            twoPlayerRapm(get_key(p1), get_key(p2), year)

from operator import itemgetter

N=150
poss_list_sample1 = dict(sorted(twoPlayer_dict_sample1.items(), key=itemgetter(1), reverse=True)[:N])
poss_list_sample2 = dict(sorted(twoPlayer_dict_sample2.items(), key=itemgetter(1), reverse=True)[:N])


def checkPos(key):
    if twoPlayer_dict_sample1[key] > minPossessions:
        return key

#print(poss_list_sample1.len)
over_possessions_sample1 = map(checkPos, poss_list_sample1)
print(over_possessions_sample1)
poss_list_master = map(checkPos, over_possessions_sample1)

arr = list(poss_list_master)

callPlayerPairs(arr, year1)
callPlayerPairs(arr, year2)

