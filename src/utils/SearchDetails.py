import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time
from multiprocessing import Process

from src.utils.GameDetails import GameDetails

load_dotenv()

class SearchDetails:
  def __init__(self, search_string):
    self.results = []
    self.num_items = 0;

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

    # Cache all games
    p_list = []
    for game in soup.find_all("a"):
      p = Process(target=self.load_game, args=(game['data-ds-appid'],))
      p_list.append(p)
      p.start()

    for p in p_list:
      p.join()

    for game in soup.find_all("a"):
      loop_start = time.perf_counter()
      try:
        details = GameDetails(game['data-ds-appid'])
      except:
        print("Error trying to load steam app id: ", game['data-ds-appid'])
      self.results.append(details)
      print(f"Game Finished in: {time.perf_counter() - loop_start:0.4f} seconds")

    print(f"Total Time: {time.perf_counter() - start:0.4f} seconds")

  def load_game(self, steamappid):
    try:
      GameDetails(steamappid)
    except:
      return