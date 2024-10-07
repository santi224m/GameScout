from src.utils.db_conn import db_conn

class db_utils:
  def insert_wishlist_item(username, steamapp_id):
    """Insert a wishlist item into the database"""
    with db_conn() as curr:
      curr.execute("INSERT INTO wishlist_item (user_account_id, steam_app_id) VALUES ((SELECT id FROM user_account WHERE username = %s), %s);", (username, steamapp_id))

  def get_user_wishlist_items(username):
    """Return a list of steam app ids from a user's wishlist"""
    with db_conn() as curr:
      curr.execute("SELECT steam_app_id FROM wishlist_item WHERE user_account_id = (SELECT id FROM user_account WHERE username = %s);", (username,))
      res = curr.fetchall()
      return res
