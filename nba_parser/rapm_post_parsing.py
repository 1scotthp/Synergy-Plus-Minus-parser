import pandas as pd
import json

year = 2018
parserPath = r"C:\Users\1scot\PycharmProjects\SPM\Synergy-Plus-Minus-parser\nba_parser"

with open(f"player_keys/{year - 1}-{year%2000}.json") as json_file:
    playerDict = json.load(json_file)

with open(f"player_keys/{year - 1}-{year%2000}_pair_count.json") as json_file2:
    twoPlayer_dict = json.load(json_file2)

def get_key(val):
    for key, value in playerDict.items():
        if val == value[0]:
            return key

df = pd.read_csv(parserPath + f"\\2-player-rapms-{year - 1}-{year%2000}\\2-player-master.csv")
df = df.iloc[::2, :]



def fix_csvs():
    new_df = []
    for index, row in df.iterrows():
        id = str(int(row["player_id"]))
        player = row["player_name"]


        [id1] = playerDict[player]
        id1 = str(int(id1))
        id = id.replace(id1, "")

        print(str(id1) + " " + id)
        player2 = get_key(int(id))


        id = int(id)
        id1 = int(id1)
        row["player_id"] = str(min(id, id1)) + " " + str(max(id,id1))
        print(str(player) + " and " + str(player2))

        new_df.append(row)

    fixed_df = pd.DataFrame(new_df)
    fixed_df.to_csv(f"fix{year - 1}-{year%2000}.csv")


fix_csvs()
##FILES
first_half = pd.read_csv("fix2016-17.csv")
second_half = pd.read_csv("fix2017-18.csv")
individual = pd.read_csv("player_rapm2016-17.csv")

def final():
    final_df = []
    for index, row in first_half.iterrows():

        combinedId = row["player_id"]

        if combinedId in second_half.values:
            id1 = int(combinedId.split()[0])
            id2 = int(combinedId.split()[1])

            player1_row = individual.loc[individual['player_id'] == id1]
            player2_row = individual.loc[individual['player_id'] == id2]
            results_row = second_half.loc[second_half['player_id'] == combinedId]

            final_row = [get_key(id1), id1, get_key(id2), id2,
                     player1_row.iloc[0]["rapm"], player1_row.iloc[0]["rapm_off"], player1_row.iloc[0]["rapm_def"],
                     player2_row.iloc[0]["rapm"], player2_row.iloc[0]["rapm_off"], player2_row.iloc[0]["rapm_def"],
                     row["rapm"], row["rapm_off"], row["rapm_def"],
                     results_row.iloc[0]["rapm"], results_row.iloc[0]["rapm_off"], results_row.iloc[0]["rapm_def"]]

            print(final_row)
            final_df.append(final_row)

    RAPM = pd.DataFrame(final_df, columns=['player 1', '1_ID', 'player 2', '2_ID',
                                           'rapm1', 'orapm1', 'drapm1', 'rapm2', 'orapm2', 'drapm2',
                                           'rapm_pair', 'orapm_pair', 'drapm_pair',
                               'rapm_pair_test', 'orapm_pair_test', 'drapm_pair_test'])
    RAPM.to_csv("RAPM.csv")

final()


