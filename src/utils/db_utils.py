from src.utils.db_conn import db_conn

class db_utils:
  def insert_wishlist_item(username, steamapp_id):
    """Insert a wishlist item into the database"""
    with db_conn() as curr:
      curr.execute("INSERT INTO wishlist_item (user_account_id, steam_app_id) VALUES ((SELECT id FROM user_account WHERE username = %s), %s) ON CONFLICT (user_account_id, steam_app_id) DO NOTHING;", (username, steamapp_id))

  def delete_wishlist_item(username, steamapp_id):
    """Remove a wishlisted item from a user's account"""
    with db_conn() as curr:
      curr.execute("DELETE FROM wishlist_item WHERE user_account_id = (SELECT id FROM user_account WHERE username =%s) AND steam_app_id = %s;", (username, steamapp_id))

  def get_user_wishlist_items(username):
    """Return a list of steam app ids from a user's wishlist"""
    with db_conn() as curr:
      curr.execute("SELECT wishlist_item.steam_app_id, added_date FROM wishlist_item INNER JOIN game ON game.steam_app_id = wishlist_item.steam_app_id WHERE user_account_id = (SELECT id FROM user_account WHERE username = %s);", (username,))
      res = curr.fetchall()
      return res

  def insert_game(steam_app_id, title):
    """Insert a game into the game table"""
    with db_conn() as curr:
      curr.execute("INSERT INTO game (steam_app_id, title) VALUES (%s, %s) ON CONFLICT (steam_app_id) DO UPDATE SET title = %s;", (steam_app_id, title, title))

  def is_game_wishlisted(username, steamapp_id):
    """Returns True if a user wishlisted the game with steamapp id, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM wishlist_item WHERE user_account_id = (SELECT id FROM user_account WHERE username = %s) AND steam_app_id = %s;", (username, steamapp_id))
      res = curr.fetchall()
      if res:
        return True
      return False
