from src.utils.GameDetails import GameDetails
from src.utils.GameCacher import GameCacher
from src.utils.db_utils import db_utils

class WishlistDetails:
  def __init__(self, username):
    self.username = username
    wishlist_data = db_utils.get_user_wishlist_items(self.username)
    self.items = []
    self.num_items = 0
    self.added_date_dict = {}

    # Cache all games
    steamappid_list = [steamid for (steamid, added_date) in wishlist_data]
    GameCacher(steamappid_list)

    # Add cached games to self.items
    for (steamid, added_date) in wishlist_data:
      self.num_items += 1
      game = GameDetails(steamid)
      self.items.append(game)
      self.added_date_dict[steamid] = added_date.strftime("%B %d, %Y")