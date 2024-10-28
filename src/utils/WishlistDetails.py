from src.utils.GameDetails import GameDetails
from src.utils.db_utils import db_utils

class WishlistDetails:
  def __init__(self):
    self.username = "user1"
    wishlist_data = db_utils.get_user_wishlist_items(self.username)
    self.items = []
    self.num_items = 0
    self.added_date_dict = {}

    for (steamid, added_date) in wishlist_data:
      self.num_items += 1
      item = GameDetails(steamid)
      self.added_date_dict[steamid] = added_date.strftime("%B %d, %Y")
      self.items.append(item)