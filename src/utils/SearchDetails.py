import time

import requests
from bs4 import BeautifulSoup

from src.utils.GameDetails import GameDetails
from src.utils.GameCacher import GameCacher

class SearchDetails:
  def __init__(self, search_string):
    self.results = []
    self.num_items = 0

    self.query_game_details(search_string)

  def query_game_details(self, search_string):
    start = time.perf_counter()
    url_params = {
          'term': search_string,
          'infinite': 1,
          'supportedlang': 'english',
          'category1': '998',
          'count': 25,
    }
    res = requests.get(f'https://store.steampowered.com/search/results/', params=url_params)
    data = res.json()
    self.num_items = data['total_count']
    soup = BeautifulSoup(data['results_html'], features="html.parser")
    print(f"Search Finished in: {time.perf_counter() - start:0.4f} seconds")

    # Store steam app id's in a list
    games = [game['data-ds-appid'] for game in soup.find_all("a")]
    GameCacher(games)

    for game_id in games:
      try:
        details = GameDetails(game_id)
        self.results.append(details)
      except:
        print("Error trying to load steam app id: ", game_id)
    print(f"Total Time: {time.perf_counter() - start:0.4f} seconds")

  def load_game(self, steamappid):
    try:
      GameDetails(steamappid)
    except:
      return