from src.utils.db_conn import db_conn

class db_utils:
  def insert_wishlist_item(username, steamapp_id):
    """Insert a wishlist item into the database"""
    with db_conn() as curr:
      curr.execute("INSERT INTO wishlist_item (user_uuid, steam_app_id) VALUES ((SELECT uuid FROM user_account WHERE username = %s), %s) ON CONFLICT (user_uuid, steam_app_id) DO NOTHING;", (username, steamapp_id))

  def delete_wishlist_item(username, steamapp_id):
    """Remove a wishlisted item from a user's account"""
    with db_conn() as curr:
      curr.execute("DELETE FROM wishlist_item WHERE user_uuid = (SELECT uuid FROM user_account WHERE username =%s) AND steam_app_id = %s;", (username, steamapp_id))

  def get_user_wishlist_items(username):
    """Return a list of steam app ids from a user's wishlist"""
    with db_conn() as curr:
      curr.execute("SELECT steam_app_id, added_date FROM wishlist_item WHERE user_uuid = (SELECT uuid FROM user_account WHERE username = %s) ORDER BY rank ASC;", (username,))
      res = curr.fetchall()
      return res

  def is_game_wishlisted(username, steamapp_id):
    """Returns True if a user wishlisted the game with steamapp id, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM wishlist_item WHERE user_uuid = (SELECT uuid FROM user_account WHERE username = %s) AND steam_app_id = %s;", (username, steamapp_id))
      res = curr.fetchall()
      if res:
        return True
      return False

  def update_wishlist_rank(username, steamappid, rank):
    """Update the rank for a game in the wishlist"""
    with db_conn() as curr:
      curr.execute("UPDATE wishlist_item SET rank = %s WHERE user_uuid = (SELECT uuid FROM user_account WHERE username = %s) AND steam_app_id = %s;", (rank, username, steamappid))