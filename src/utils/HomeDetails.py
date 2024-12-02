import time

import requests
import json

from src.utils.GameDetails import GameDetails
from src.utils.GameCacher import GameCacher

class HomeDetails:
  def __init__(self):
    self.featured = []
    self.trending = []
    self.under5 = []
    self.cut50 = []

    self.query_game_details()

  def query_game_details(self):
    start = time.perf_counter()
    res = requests.get(f'https://isthereanydeal.com/home/api/page-1/')
    data = res.json()

    featured_ids = data['gids']['highlights']
    trending_ids = data['gids']['trending']
    under5_ids = data['gids']['price5']
    cut50_ids = data['gids']['cut50']

    print(f"ITAD Data Finished in: {time.perf_counter() - start:0.4f} seconds")

    wacky_id_conversion = featured_ids + trending_ids + under5_ids + cut50_ids

    id_res = requests.post(f'https://api.isthereanydeal.com/lookup/shop/61/id/v1', data=json.dumps(wacky_id_conversion))
    id_data = id_res.json()

    featured_steam_ids = data['gids']['highlights']
    trending_steam_ids = data['gids']['trending']
    under5_steam_ids = data['gids']['price5']
    cut50_steam_ids = data['gids']['cut50']

    temp = []
    for id in featured_ids:
      if id_data[id] is not None: temp.append(next((s for s in id_data[id] if 'app' in s), None))
    featured_steam_ids = [int(x.split('/')[1]) for x in temp if x is not None]
    
    temp = []
    for id in trending_ids:
      if id_data[id] is not None: temp.append(next((s for s in id_data[id] if 'app' in s), None))
    trending_steam_ids = [int(x.split('/')[1]) for x in temp if x is not None]
    
    temp = []
    for id in under5_ids:
      if id_data[id] is not None: temp.append(next((s for s in id_data[id] if 'app' in s), None))
    under5_steam_ids = [int(x.split('/')[1]) for x in temp if x is not None]
    
    temp = []
    for id in cut50_ids:
      if id_data[id] is not None: temp.append(next((s for s in id_data[id] if 'app' in s), None))
    cut50_steam_ids = [int(x.split('/')[1]) for x in temp if x is not None]

    print(f"ID Parsing Finished in: {time.perf_counter() - start:0.4f} seconds")

    wacky_game_caching = featured_steam_ids + trending_steam_ids + under5_steam_ids + cut50_steam_ids

    GameCacher(wacky_game_caching)
    
    for game_id in featured_steam_ids:
        details = GameDetails(game_id)
        self.featured.append(details)
    
    for game_id in trending_steam_ids:
        details = GameDetails(game_id)
        self.trending.append(details)

    for game_id in under5_steam_ids:
        details = GameDetails(game_id)
        self.under5.append(details)
    
    for game_id in cut50_steam_ids:
        details = GameDetails(game_id)
        self.cut50.append(details)
    
    print(f"Total Time: {time.perf_counter() - start:0.4f} seconds")