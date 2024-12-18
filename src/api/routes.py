from flask import request, jsonify, session
from src.api import bp
from src.utils.db_utils import db_utils
from src.utils.ITADHelper import ITADHelper

@bp.route('/add_wishlist_item', methods=('GET', 'POST'))
def add_wishlist_item():
  steamapp_id = request.json['steamapp_id']
  username = session['user']['username']
  db_utils.insert_wishlist_item(username, steamapp_id)
  return jsonify({'status': 'success'})

@bp.route('/delete_wishlist_item', methods=('GET', 'POST'))
def delete_wishlist_item():
  steamapp_id = request.json['steamapp_id']
  username = session['user']['username']
  db_utils.delete_wishlist_item(username, steamapp_id)
  return jsonify({'status': 'success'})

@bp.route('/add_watchlist_item', methods=('GET', 'POST'))
def add_watchlist_item():
  steamapp_id = request.json['steamapp_id']
  username = session['user']['username']
  db_utils.insert_watchlist_item(username, steamapp_id)
  return jsonify({'status': 'success'})

@bp.route('/delete_watchlist_item', methods=('GET', 'POST'))
def delete_watchlist_item():
  steamapp_id = request.json['steamapp_id']
  username = session['user']['username']
  db_utils.delete_watchlist_item(username, steamapp_id)
  return jsonify({'status': 'success'})

@bp.route('/get_wishlist_items', methods=('GET', 'POST'))
def get_wishlist_items():
  username = session['user']['username']
  res = db_utils.get_user_wishlist_items(username)
  return jsonify(res)

@bp.route('/is_game_wishlisted', methods=('GET', 'POST'))
def is_game_wishlisted():
  if "user" not in session: return {"error": 500}
  username = session['user']['username']
  steamapp_id = request.json['steamapp_id']
  res = db_utils.is_game_wishlisted(username, steamapp_id)
  return jsonify(res)

@bp.route('/is_game_watchlisted', methods=('GET', 'POST'))
def is_game_watchlisted():
  if "user" not in session: return {"error": 500}
  username = session['user']['username']
  steamapp_id = request.json['steamapp_id']
  res = db_utils.is_game_watchlisted(username, steamapp_id)
  return jsonify(res)

@bp.route('/update_wishlist_rank', methods=('GET', 'POST'))
def update_wishlist_rank():
  username = session['user']['username']
  for steamappid, rank in request.json.items():
    db_utils.update_wishlist_rank(username, steamappid, rank)
  return jsonify({'status': 'success'})

@bp.route('/get_prices', methods=('GET', 'POST'))
def get_prices():
  """Return prices for game"""
  try:
    steamappid = request.json["steam_app_id"]
    res = ITADHelper(steamappid)
  except Exception as e:
    return jsonify({"success": False, "error": e})

  return jsonify({"success": True, "deals": res.deals})