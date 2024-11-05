from multiprocessing import Process

from src.utils.GameDetails import GameDetails
from src.utils.db_utils import db_utils

class WishlistDetails:
  def __init__(self, username):
    self.username = username
    wishlist_data = db_utils.get_user_wishlist_items(self.username)
    self.items = []
    self.num_items = 0
    self.added_date_dict = {}

    # Load all games using multiprocessing first to cache them
    p_list = []
    for (steamid, added_date) in wishlist_data:
      p = Process(target=self.load_game, args=(steamid,))
      p_list.append(p)
      p.start()

    # Wait for all games to load
    for p in p_list:
      p.join()

    # Add cached games to self.items
    for (steamid, added_date) in wishlist_data:
      self.num_items += 1
      game = GameDetails(steamid)
      self.items.append(game)
      self.added_date_dict[steamid] = added_date.strftime("%B %d, %Y")

  def load_game(self, steamappid):
    GameDetails(steamappid)
