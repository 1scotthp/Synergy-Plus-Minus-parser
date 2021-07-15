import quandl
import pandas as pd
import pymongo
from pymongo import MongoClient
import nba_parser as npar
import numpy as numpy
#import nba_scraper.nba_scraper as ns
import sys
# insert at 1, 0 is the script path (or '' in REPL)
#sys.path.insert(1, 'Synergy_Plus_Minus_scraper/nba_scraper/')

from Synergy_Plus_Minus_scraper.nba_scraper.nba_scraper import scrape_game
import pdmongo as pdm


def mongoScrapeSeason(year):
  game_ids = list(range(int(f"2{year - 2001}00001"), int(f"2{year - 2001}01231")))
  pbp_objects = []
  i = 0
  for game_id in game_ids:
      game_df = scrape_game([game_id])
      pbp = npar.PbP(game_df)
      pbp_objects.append(pbp)
      if game_id % 10 == 0:
        rapm_possession = pd.concat([x.rapm_possessions() for x in pbp_objects])
        rapm_possession.to_mongo(str(game_id), f"mongodb://localhost:27017/{year - 1}-{year%2000}")
        pbp_objects = []


def mongoScrapeSeasonFullBox(year):
  game_ids = list(range(int(f"2{year - 2001}00001"), int(f"2{year - 2001}01231")))
  pbp_objects = []
  i = 0
  for game_id in game_ids:
    if game_id > 21600750:
      game_df = scrape_game([game_id])
      pbp = npar.PbP(game_df)
      pbp_objects.append(pbp)
      if game_id % 10 == 0:
        r = pd.concat([x.df for x in pbp_objects])
        r.to_csv("test.csv")
        n = pd.read_csv("test.csv")
        n.to_mongo(str(game_id), f"mongodb://localhost:27017/{year - 1}-{year % 2000}_Full_Box_Score")



mongoScrapeSeasonFullBox(2017)




