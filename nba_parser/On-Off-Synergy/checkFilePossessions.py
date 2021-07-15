import pandas as pd
import json


year = 2018
file = f"2-player-rapms-{year - 1}-{year%2000}/2-player-master.csv"

with open(f'player_keys/{year - 1}-{year%2000}.json') as json_file:
    playerDict = json.load(json_file)

with open(f'player_keys/{year - 1}-{year%2000}_pair_count.json') as json_file:
    twoplayerDict = json.load(json_file)

def get_key(val):
    for key, value in playerDict.items():
        if val == value[0]:
            return key


df = pd.read_csv(file)
new_df = []
for index, row in df.iterrows():
    print(int(row["player_id"]))
    id = str(int(row["player_id"]))
    player = row["player_name"]

    if playerDict.get(player):
        [id1] = playerDict[player]
        id1 = str(int(id1))
        id = id.replace(id1, "")


        id1 = int(id1)
        id = int(id)
        a = str(min(id1, id)) + "-" + str(max(id, id1))

        if twoplayerDict.get(a) and twoplayerDict[a]> 2000:
            new_df.append(row)

final = pd.DataFrame(new_df)
final.to_csv(file)


