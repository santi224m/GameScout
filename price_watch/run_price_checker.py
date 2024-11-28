"""
Check prices for all games in price_watch table and email user if price drops
below their desired price.
"""
from db_conn import db_conn

def get_price_watch_list():
  with db_conn() as curr:
    curr.execute("""
      SELECT
        email,
        steam_app_id,
        desired_price,
        last_seen_price
      FROM price_watch
      INNER JOIN user_account
        ON user_account.uuid = price_watch.user_uuid;
      """)
    res = curr.fetchall()
    l = [{'email': price_watch[0], 'steam_app_id': price_watch[1], 'desired_price': price_watch[2], 'last_seen_price': price_watch[3]} for price_watch in res]
    return l

def get_lowest_price(steam_app_id):
  """Return the lowest price for the game using the ITAD API"""
  raise NotImplementedError

if __name__ == "__main__":
  price_watch_list = get_price_watch_list()
  prices_cache = {} # Store prices to use for duplicate games

  for game in price_watch_list:
    print(game)