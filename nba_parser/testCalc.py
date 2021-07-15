import nba_scraper.nba_scraper as ns
import nba_parser as npar
import pandas as pd
from pymongo import MongoClient
import pdmongo as pdm
client = MongoClient('localhost', 27017)

import nba_scraper.nba_scraper as ns
import nba_parser as npar

pbg_dfs = []
pbp_objects = []
for game_id in range(20700001, 20700010):
    game_df = ns.scrape_game([game_id])
    pbp = npar.PbP(game_df)
    pbp_objects.append(pbp)
    player_stats = pbp.playerbygamestats()
    pbg_dfs.append(player_stats)

player_totals = npar.PlayerTotals(pbg_dfs)

#produce a dataframe of eFG%, TS%, TOV%, OREB%, AST%, DREB%,
#STL%, BLK%, USG%, along with summing the other
#stats produced by the playerbygamestats() method to allow further
#calculations

player_adv_stats = player_totals.player_advanced_stats()
player_adv_stats.to_csv("test.csv")


#to calculate a RAPM regression for players first have to calculate
#RAPM possessions from the list of PbP objects we collected above

rapm_possession = pd.concat([x.rapm_possessions() for x in pbp_objects])




player_rapm_df = npar.PlayerTotals.player_rapm_results(rapm_possession).drop_duplicates()

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
