"""Threaded API calls for GameDetails.py"""
import logging
import threading
import requests
import time
import json
import os

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

class GDThreadedAPI:
  def __init__(self, steamappid):
    start = time.perf_counter()
    self.steamappid = steamappid
    self.steam_api_res = None
    self.steam_reviews_api_res = None
    self.ITAD_api_1_res = None
    self.ITAD_api_3_res = None

    thread_ITAD_api_1 = threading.Thread(target=self.get_ITAD_api_1)
    thread_ITAD_api_1.start()
    thread_steamapi = threading.Thread(target=self.get_steamapi)
    thread_steamapi.start()
    thread_steamreviewsapi = threading.Thread(target=self.get_steam_reviews_api)
    thread_steamreviewsapi.start()
    thread_ITAD_api_3 = threading.Thread(target=self.get_ITAD_api_3)
    thread_ITAD_api_1.join()
    thread_ITAD_api_3.start()

    thread_steamapi.join()
    thread_steamreviewsapi.join()
    thread_ITAD_api_3.join()

    end = time.perf_counter()
    logging.info(f"GDThreadedAPI: Total time {end - start:0.4f} seconds")

  def get_steamapi(self):
    logging.info("SteamAPI: Starting request")
    usd = 1
    url_params = {'appids': self.steamappid, 'currency': usd}
    self.steam_api_res = requests.get('https://store.steampowered.com/api/appdetails', params=url_params)
    logging.info("SteamAPI: Received response")

  def get_steam_reviews_api(self):
    logging.info("SteamReviewsAPI: Starting request")
    url_params = {
      'appids': self.steamappid,
      'json': 1,
      'filter': 'all',
      'language': 'english',
      'purchase_type': 'all',
      'review_type': 'all',
      'num_per_page': 10
    }
    self.steam_reviews_api_res = requests.get(f'https://store.steampowered.com/appreviews/{self.steamappid}', params=url_params)
    logging.info("SteamReviewsAPI: Received Request")

  def get_ITAD_api_1(self):
    logging.info("ITADapi1: Starting request")
    app_format =  'app/' + str(self.steamappid)
    payload = [app_format]
    self.ITAD_api_1_res = requests.post('https://api.isthereanydeal.com/lookup/id/shop/61/v1', data=json.dumps(payload))
    logging.info("ITADapi1: Received Request")

  def get_ITAD_api_3(self):
    logging.info("ITADapi3: Starting request")
    app_format =  'app/' + str(self.steamappid)
    appid = self.ITAD_api_1_res.json()[app_format]
    url_params = {
      "key": os.getenv("ITAD_API_KEY"),
      "id": appid
    }
    self.ITAD_api_3_res = requests.get('https://api.isthereanydeal.com/games/info/v2', params=url_params)
    logging.info("ITADapi3: Received Request")