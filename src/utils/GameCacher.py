"""
Pass in a list of steam app id's to the GameCacher class to quickly
cache all of them using multiprocessing.
"""
from multiprocessing import Process

from src.utils.GameDetails import GameDetails

class GameCacher:
  def __init__(self, steamappid_list):
    p_list = []
    for steamappid in steamappid_list:
      p = Process(target=self.cache_game, args=(steamappid,))
      p_list.append(p)
      p.start()

    # Wait for all games to load
    for p in p_list:
      p.join()

  def cache_game(self, steamappid):
    GameDetails(steamappid)