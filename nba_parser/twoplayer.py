import nba_scraper.nba_scraper as ns
import nba_parser as npar
import pandas as pd
from pymongo import MongoClient
import pdmongo as pdm
client = MongoClient()
client = MongoClient('localhost', 27017)

# make sure id1 > id2
def checkPlayer(id1, id2, row):
    count = 0
    for column in row:
        if column == id1 or column == id2:
            count += 1
    if count >= 2:
        row = row.replace(id1, int(str(id1) + str(id2)))
        row = row.replace(id2, int(str(id1) + str(id2)))
    return row

def twoPlayerParser(rapm_shifts, id1, id2):
    new_df = []
    for index, row in rapm_shifts.iterrows():
        temp = checkPlayer(id1,id2, row)
        new_df.append(temp)
    return pd.DataFrame(new_df)



def runTwoPlayer(id1, id2, year):
    game_ids = list(range(int(f"2{year - 2001}00001"), int(f"2{year - 2001}01231")))
    collection_ids = list(filter(lambda x: x % 10==0, game_ids))

    pbp_objects = []
    i = 0
    for collection_id in collection_ids:
        print(collection_id)
        df = pdm.read_mongo(str(collection_id), [], f"mongodb://localhost:27017/{year - 1}-{year%2000}")
        new_df = twoPlayerParser(df, id1, id2)
        pbp_objects.append(new_df)

    rapm_possession = pd.concat([x for x in pbp_objects])

    return rapm_possession


