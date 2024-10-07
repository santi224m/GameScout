from flask import request, jsonify
from src.api import bp
from src.utils.db_utils import db_utils

@bp.route('/add_wishlist_item', methods=('GET', 'POST'))
def add_wishlist_item():
  steamapp_id = request.json['steamapp_id']
  username = "user1"
  db_utils.insert_wishlist_item(username, steamapp_id)
  return jsonify({'status': 'success'})

@bp.route('/get_wishlist_items', methods=('GET', 'POST'))
def get_wishlist_items():
  username = "user1"
  res = db_utils.get_user_wishlist_items(username)
  return jsonify(res)