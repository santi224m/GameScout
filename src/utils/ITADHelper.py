"""Is There Any Deal API Helper"""
import json
import os
from dotenv import load_dotenv
from flask import session

import requests
from src.utils.db_utils import db_utils

load_dotenv()

class ITADHelper:
  def __init__(self, steamappid):
    self.steamappid = steamappid
    self.itad_id = self.get_itad_id(self.steamappid)
    self.deals = self.get_itad_prices(self.itad_id)

  def get_itad_id(self, steamappid):
    """Return ITAD ID"""
    itad_id = db_utils.get_itad_game_id(steamappid)
    itad_id = None # Temp overide to implement below
    if itad_id is not None:
      return itad_id

    api_url = 'https://api.isthereanydeal.com/lookup/id/shop/61/v1'
    key =  'app/' + str(steamappid)
    payload = [key]
    res = requests.post(api_url, data=json.dumps(payload))
    return res.json()[key]

  def get_itad_prices(self, itad_id):
    """Return ITAD prices"""
    api_url = "https://api.isthereanydeal.com/games/prices/v2"
    payload = [itad_id]
    url_params = {
      "key": os.getenv("ITAD_API_KEY"),
      "country": "US",
      "nondeals": "true",
      "vouchers": "true"
    }
    if 'user' in session: url_params['country'] = session['user']['country']
    res = requests.post(api_url, data=json.dumps(payload), params=url_params)
    deals = {deal['shop']['name']: {'current_price': deal['price']['amount'], 'regular_price': deal['regular']['amount'], 'discount': deal['cut'], 'voucher': deal['voucher'], 'url': deal['url']} for deal in res.json()[0]['deals']}
    return deals