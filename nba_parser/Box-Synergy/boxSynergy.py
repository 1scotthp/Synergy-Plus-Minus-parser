import nba_scraper.nba_scraper as ns
import nba_parser as npar
import pandas as pd
from pymongo import MongoClient
import pdmongo as pdm
client = MongoClient()
client = MongoClient('localhost', 27017)

# make sure id1 > id2
def checkPlayerBox(id1, id2, row):
    count = 0
    for j in range(5):
        if row[f"home_player_{j + 1}_id"] == id1 or row[f"home_player_{j + 1}_id"] == id2:
             count+=1

    if count > 1:
        return True

    count = 0
    for j in range(5):
        if row[f"away_player_{j + 1}_id"] == id1 or row[f"away_player_{j + 1}_id"] == id2:
            count += 1
    if count > 1:
        return True

    return False



def twoPlayerParserBox(rapm_shifts, id1, id2):
    new_df = []
    for index, row in rapm_shifts.iterrows():
        check = checkPlayerBox(id1,id2, row)
        if check:
            new_df.append(row)
    return pd.DataFrame(new_df)



def runTwoPlayerBox(id1, id2, year):
    game_ids = list(range(int(f"2{year - 2001}00001"), int(f"2{year - 2001}01231")))
    collection_ids = list(filter(lambda x: x % 10==0, game_ids))

    pbp_objects = []
    for collection_id in collection_ids:
            print(collection_id)
            df = pdm.read_mongo(str(collection_id), [], f"mongodb://localhost:27017/{year - 1}-{year%2000}_Full_Box")
            df.to_csv("check.csv")
            new_df = twoPlayerParserBox(df, id1, id2)
            pbp_objects.append(new_df)


    box_possession = pd.concat([x for x in pbp_objects])

    return box_possession


import nba_scraper.nba_scraper as ns
import nba_parser as npar

year = 2017
def runRegularBPM():
    game_ids = list(range(int(f"2{year - 2001}00001"), int(f"2{year - 2001}01231")))
    collection_ids = list(filter(lambda x: x % 10 == 0, game_ids))
    pbp_objects = []
    pbg_dfs = []
    i = 0
    for collection_id in collection_ids:
      if i < 4:
        print(collection_id)
        df = pdm.read_mongo(str(collection_id), [], f"mongodb://localhost:27017/{year - 1}-{year % 2000}_Full_Box_Score")
        for j in range(10):
            #df_game = df.loc[df['game_id'] == collection_id-9+i]
            pbp = npar.PbP(df[df.game_id == collection_id-9+i].copy())
            player_stats = pbp.playerbygamestats()
            pbg_dfs.append(player_stats)
      i += 1

    player_totals = npar.PlayerTotals(pbg_dfs)
    player_totals.df.to_csv("test.csv")

    # produce a dataframe of eFG%, TS%, TOV%, OREB%, AST%, DREB%,
    # STL%, BLK%, USG%, along with summing the other
    # stats produced by the playerbygamestats() method to allow further
    # calculations

    player_adv_stats = player_totals.player_advanced_stats()
    player_adv_stats.to_csv("2016-17_advanced.csv")


runRegularBPM()