import nba_scraper.nba_scraper as ns
import nba_parser as npar
import pandas as pd
from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)

#0022000386, 0022000705, 0022000898
pbg_dfs = []
pbp_objects = []
for game_id in range(22000001, 22000020):
    game_df = ns.scrape_game([game_id])
    pbp = npar.PbP(game_df)
    pbp_objects.append(pbp)
    #player_stats = pbp.playerbygamestats()
    #pbg_dfs.append(player_stats)

rapm_possession = pd.concat([x.rapm_possessions() for x in pbp_objects])
rapm_possession.to_csv("2020-21_1.csv")


# make sure id1 > id2
def checkPlayer(id1, id2, row):
    combinedId = int(str(id1) + str(id2))
    count = 0
    for column in row:
        if column == id1 or column == id2:
            count += 1
    if count >= 2:
        row = row.replace(id1, combinedId)
        row = row.replace(id2, combinedId)
    return row


def twoPlayerParser(rapm_shifts):
    new_df = []
    for index, row in rapm_shifts.iterrows():
        temp = checkPlayer(1495, 2225, row)
        new_df.append(temp)
    return pd.DataFrame(new_df)



final_pbp_objects = []
for x in pbp_objects:
    y = twoPlayerParser(x.rapm_possessions())
    final_pbp_objects.append(y)



rapm_possession = pd.concat([x for x in final_pbp_objects])

rapm_possession.to_csv("long.csv")


player_rapm_df = npar.PlayerTotals.player_rapm_results(rapm_possession)

player_rapm_df.to_csv("player_rapm.csv")


# game_df = ns.scrape_game([21800001, 21800002])
# pbp = npar.PbP(game_df)
# player_stats = pbp.playerbygamestats()
#
# #can also derive single possessions for RAPM calculations
#
# rapm_shifts = pbp.rapm_possessions()
# rapm_shifts.to_csv("2020-21.csv")
#
# player_rapm_df = npar.PlayerTotals.player_rapm_results(rapm_shifts)
# player_rapm_df.to_csv("e.csv")
