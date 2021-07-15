import nba_scraper.nba_scraper as ns
import nba_parser as npar
import pandas as pd
from pymongo import MongoClient
import pdmongo as pdm
client = MongoClient()
client = MongoClient('localhost', 27017)
import json
from boxSynergy import runTwoPlayerBox



year1 = 2017
year2 = 2018
minPossessions = 2000


twoPlayer_path_sample1 = f"{year1 - 1}-{year1 % 2000}_pair_count.json"

# with open('player_keys/2016-17.json') as json_file:
#     playerDict = json.load(json_file)
#
with open(twoPlayer_path_sample1) as json_file2:
     twoPlayer_dict_sample1 = json.load(json_file2)
#

#2544,Kevin Love,201567



from operator import itemgetter

N=150
poss_list_sample1 = dict(sorted(twoPlayer_dict_sample1.items(), key=itemgetter(1), reverse=True)[:N])



pbg_dfs = []
pbp_dfs = runTwoPlayerBox(2544, 201567, 2017)
pbp_dfs.to_csv("LebLove.csv")
pbp = npar.PbP(pbp_dfs)
player_stats = pbp.playerbygamestats()
pbg_dfs.append(player_stats)

player_totals = npar.PlayerTotals(pbg_dfs)

#produce a dataframe of eFG%, TS%, TOV%, OREB%, AST%, DREB%,
#STL%, BLK%, USG%, along with summing the other
#stats produced by the playerbygamestats() method to allow further
#calculations

player_adv_stats = player_totals.player_advanced_stats()

player_adv_stats.to_csv("adv.csv")







#produce a dataframe of eFG%, TS%, TOV%, OREB%, AST%, DREB%,
#STL%, BLK%, USG%, along with summing the other
#stats produced by the playerbygamestats() method to allow further
#calculations

player_adv_stats = player_totals.player_advanced_stats()