from src.utils.db_conn import db_conn

class db_utils:
  def insert_wishlist_item(username, steamapp_id):
    """Insert a wishlist item into the database"""
    with db_conn() as curr:
      curr.execute("INSERT INTO wishlist_item (user_account_id, steam_app_id) VALUES ((SELECT id FROM user_account WHERE username = %s), %s) ON CONFLICT (user_account_id, steam_app_id) DO NOTHING;", (username, steamapp_id))

  def get_user_wishlist_items(username):
    """Return a list of steam app ids from a user's wishlist"""
    with db_conn() as curr:
      curr.execute("SELECT wishlist_item.steam_app_id, game.title FROM wishlist_item INNER JOIN game ON game.steam_app_id = wishlist_item.steam_app_id WHERE user_account_id = (SELECT id FROM user_account WHERE username = %s);", (username,))
      res = curr.fetchall()
      return res

  def insert_game(steam_app_id, title):
    """Insert a game into the game table"""
    with db_conn() as curr:
      curr.execute("INSERT INTO game (steam_app_id, title) VALUES (%s, %s) ON CONFLICT (steam_app_id) DO UPDATE SET title = %s;", (steam_app_id, title, title))