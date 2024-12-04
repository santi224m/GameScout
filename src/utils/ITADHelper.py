"""Is There Any Deal API Helper"""
import json
import os

import requests
from src.utils.db_utils import db_utils

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
    res = requests.post(api_url, data=json.dumps(payload), params=url_params)
    return res.json()[0]['deals']