import requests
from bs4 import BeautifulSoup
import os
import math
import json
from dotenv import load_dotenv

load_dotenv()

class SearchDetails:
  def __init__(self, search_string):
    self.results = []

    self.query_steam_search(search_string)
    self.query_itad()
    # self.query_steamspy()


  def query_steam_search(self, search_string):
    url_params = {
          'term': search_string,
          'infinite': 1,
          'supportedlang': 'english',
          'category1': '998',
          'count': 50,
    }
    res = requests.get(f'https://store.steampowered.com/search/results/', params=url_params)
    data = res.json()['results_html']
    soup = BeautifulSoup(data, features="html.parser")

    for tag in soup.find_all("a"):
      result = {}
      # Title
      result['title'] = tag.span.string
      # Steam ID
      result['steamid'] = tag['data-ds-appid']
      # Banner Img
      result['banner_img'] = tag.find("img")['srcset'].split(" ")[2]
      # Release Date
      result['release_date'] = tag.find("div", class_="search_released").string.strip()
      # Platforms
      result['platforms'] = {
        'windows': False,
        'mac': False,
        'linux': False
      }
      for platform in tag.find_all(class_="platform_img"):
        if platform["class"][1] == "win":
          result['platforms']['windows'] = True
        if platform["class"][1] == "mac":
          result['platforms']['mac'] = True
        if platform["class"][1] == "linux":
          result['platforms']['linux'] = True
        
      self.results.append(result)


  def query_steamspy(self):
    for result in self.results:
      url_params = {'request': 'appdetails', 'appid':result['steamid']}
      res = requests.get('https://steamspy.com/api.php', params=url_params)
      app_data = res.json()

      result['tags'] = [tag for tag in app_data['tags']]
      result['total_reviews'] = app_data['positive'] + app_data['negative']
      result['total_positive'] = app_data['positive']
      result['total_negative'] = app_data['negative']

  def query_itad(self):
    payload = ["app/" + result['steamid'] for result in self.results]
    res = requests.post('https://api.isthereanydeal.com/lookup/id/shop/61/v1', data=json.dumps(payload))
    app_data = res.json()
    
    headers = {
      'key': os.getenv("ITAD_API_KEY"),
      'id': app_data['app/400']
    }
    res = requests.get('https://api.isthereanydeal.com/games/info/v2', headers=headers)
    data = res.json()
    print(str(data))

data = SearchDetails("portal")