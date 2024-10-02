import requests
from bs4 import BeautifulSoup
import os
import math
import json
from dotenv import load_dotenv
import time

load_dotenv()

class SearchDetails:
  def __init__(self, search_string):
    self.results = []

    self.query_steam_search(search_string)
    # self.query_itad()
    # self.query_steamspy()


  def query_steam_search(self, search_string):
    start = time.perf_counter()
    url_params = {
          'term': search_string,
          'infinite': 1,
          'supportedlang': 'english',
          'category1': '998',
          'count': 25,
    }
    res = requests.get(f'https://store.steampowered.com/search/results/', params=url_params)
    data = res.json()['results_html']
    soup = BeautifulSoup(data, features="html.parser")

    print(f"Search Finished in: {time.perf_counter() - start:0.4f} seconds")

    for game in soup.find_all("a"):
      game_start = time.perf_counter()
      result = {}
      # Title
      result['title'] = game.span.string
      # Steam ID
      result['steamid'] = game['data-ds-appid']
      # Banner Img
      result['banner_img'] = game.find("img")['srcset'].split(" ")[2]
      # Release Date
      result['release_date'] = game.find("div", class_="search_released").string.strip()
      # Platforms
      result['platforms'] = {
        'windows': False,
        'mac': False,
        'linux': False
      }
      for platform in game.find_all(class_="platform_img"):
        if platform['class'][1] == "win":
          result['platforms']['windows'] = True
        if platform['class'][1] == "mac":
          result['platforms']['mac'] = True
        if platform['class'][1] == "linux":
          result['platforms']['linux'] = True

      # Get Tags
      tags = []
        
      self.results.append(result)
      res = requests.get(f'https://store.steampowered.com/apphover/{game['data-ds-appid']}')
      tag_data = BeautifulSoup(res._content, features="html.parser")

      for tag in tag_data.find_all(class_="app_tag"):
        tags.append(tag.string)

      result['tags'] = tags

      print(f"Game Finished in: {time.perf_counter() - game_start:0.4f} seconds")
    
    print(f"Total Time: {time.perf_counter() - start:0.4f} seconds")


  # def query_steamspy(self):
  #   for result in self.results:
  #     url_params = {'request': 'appdetails', 'appid':result['steamid']}
  #     res = requests.get('https://steamspy.com/api.php', params=url_params)
  #     app_data = res.json()

  #     result['tags'] = [tag for tag in app_data['tags']]
  #     result['total_reviews'] = app_data['positive'] + app_data['negative']
  #     result['total_positive'] = app_data['positive']
  #     result['total_negative'] = app_data['negative']

  # def query_itad(self):
  #   payload = ["app/" + result['steamid'] for result in self.results]
  #   res = requests.post('https://api.isthereanydeal.com/lookup/id/shop/61/v1', data=json.dumps(payload))
  #   app_data = res.json()
    
  #   url_params = {
  #     'key': os.getenv("ITAD_API_KEY"),
  #     'id': app_data['app/400']
  #   }
  #   res = requests.get('https://api.isthereanydeal.com/games/info/v2', params=url_params)
  #   data = res.json()
  #   print(str(data))