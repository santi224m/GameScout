"""The GameDetails class collects and stores game info using various APIs"""
import requests
import math
import os
from howlongtobeatpy import HowLongToBeat
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import time
from fake_useragent import UserAgent
import json
from datetime import datetime
import redis
import pickle
import re

load_dotenv()

class GameDetails :
  def __init__(self, steam_app_id):
    start = time.perf_counter()

    if isinstance(steam_app_id, str) and not steam_app_id.isdigit():
      raise ValueError("Steam App ID must be a digit")
    
    # Steam Info
    self.steam_app_id = str(steam_app_id)
    self.title = None
    self.short_description = None
    self.detailed_description = None
    self.header_img = None
    self.developers = None
    self.publishers = None
    self.platforms = {
      'windows': False,
      'mac': False,
      'linux': False
    }
    self.pc_requirements = {
      'minimum': None,
      'recommended': None
    }
    self.mac_requirements = {
      'minimum': None,
      'recommended': None
    }
    self.linux_requirements = {
      'minimum': None,
      'recommended': None
    }
    self.metacritic = None
    self.legal_notice = None
    self.categories = []
    self.screenshots = []
    self.achievements = None
    self.release_date = None
    self.esrb_rating = None

    # ITAD
    self.deals = []
    self.tags = []
    self.is_reviews = False
    self.total_reviews = None
    self.positive_reviews = None
    self.negative_reviews = None    

    # Steam Reviews
    self.reviews = []
    
    # HowLongToBeat
    self.hltb = {
      'link': None,
      'main': None,
      'main_extra': None,
      'completionist': None,
      'all_styles': None
    }
    init_end = time.perf_counter()
    print(f"Init variables in {init_end - start:0.4f} seconds")

    # Connect to Redis
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    # See if the Steam ID is already in Redis
    if (game_cache := redis_conn.get(steam_app_id)) is not None:
      print("Using game cache...")
      game = pickle.loads(game_cache)
      # Copy Redis Data into this GameDetails Instance
      self.__dict__ = game.__dict__.copy()
      end = time.perf_counter()
      print(f"Total Time: {end - start:0.4f} seconds")
    else:
      # If not in Redis, get it the old fashioned way
      steam_data = query_steam_api(self.steam_app_id)
      steam_end = time.perf_counter()
      print(f"Gathered Steam Data in {steam_end - init_end:0.4f} seconds")

      # steamspy_data = query_steamspy_api(self.steam_app_id)
      # steamspy_end = time.perf_counter()
      # print(f"Gathered SteamSpy Data in {steamspy_end - steam_end:0.4f} seconds")

      reviews_data = query_steam_reviews_api(self.steam_app_id)
      reviews_end = time.perf_counter()
      print(f"Gathered Reviews Data in {reviews_end - steam_end:0.4f} seconds")

      reviews_data = parse_steam_ids(reviews_data)
      parse_reviews_end = time.perf_counter()
      print(f"Updated Reviews Data in {parse_reviews_end - reviews_end:0.4f} seconds")

      itad_data = query_itad_api(self.steam_app_id, steam_data['release_date']['coming_soon'])
      itad_end = time.perf_counter()
      print(f"Gathered ITAD Data in {itad_end - parse_reviews_end:0.4f} seconds")

      # cheap_shark_data = query_cheap_shark_api(self.steam_app_id)
      # cheapshark_end = time.perf_counter()

      # hltb_data = query_hltb_manual(steam_data['name'])
      hltb_data = query_hltb(steam_data['name'])
      hltb_end = time.perf_counter()
      print(f"Gathered HLTB in {hltb_end - itad_end:0.4f} seconds")

      self.update(steam_data, reviews_data, itad_data, hltb_data)
      update_end = time.perf_counter()
      print(f"Update variables in {update_end - hltb_end:0.4f} seconds")
      
      print(f"Total Time: {update_end - start:0.4f} seconds")

      # Store game_details in Redis cache
      game_cache = pickle.dumps(self)
      redis_conn.set(steam_app_id, game_cache)
      HOUR_SECONDS = 3600
      redis_conn.expire(steam_app_id, HOUR_SECONDS)

  def update(self, steam_data, reviews_data, itad_data, hltb_data):
    """Update GameDetails with data from our various API's"""

    # Steam
    self.title = steam_data['name']
    self.short_description = steam_data['short_description']
    self.detailed_description = soupificate(steam_data['detailed_description'])
    self.header_img = steam_data['header_image']
    self.developers = ', '.join(steam_data['developers'])
    self.publishers = ', '.join(steam_data['publishers'])
    self.platforms = steam_data['platforms']
    if self.platforms['windows']:
      for req in steam_data['pc_requirements']:
        steam_data['pc_requirements'][req] = soupify(steam_data['pc_requirements'][req])
      self.pc_requirements = steam_data['pc_requirements']
    if self.platforms['mac']:
      for req in steam_data['mac_requirements']:
        steam_data['mac_requirements'][req] = soupify(steam_data['mac_requirements'][req])
      self.mac_requirements = steam_data['mac_requirements']
    if self.platforms['linux']:
      for req in steam_data['linux_requirements']:
        steam_data['linux_requirements'][req] = soupify(steam_data['linux_requirements'][req])
      self.linux_requirements = steam_data['linux_requirements']
    if 'legal_notice' in steam_data:
      self.legal_notice = steam_data['legal_notice']
    if 'metacritic' in steam_data:
      self.metacritic = steam_data['metacritic']
      if int(self.metacritic['score']) >= 75: self.metacritic['color'] = "green"
      elif int(self.metacritic['score']) >= 50: self.metacritic['color'] = "yellow"
      else: self.metacritic['color'] = "red"
    self.categories = steam_data['categories']
    self.screenshots = steam_data['screenshots']
    if 'achievements' in steam_data:
      self.achievements = steam_data['achievements']
    self.release_date = steam_data['release_date']
    if steam_data['ratings'] and 'esrb' in steam_data['ratings']:
      self.esrb_rating = steam_data['ratings']['esrb']
      if 'interactive_elements' not in self.esrb_rating:
        self.esrb_rating['interactive_elements'] = None
      if 'descriptors' not in self.esrb_rating:
         self.esrb_rating['descriptors'] = None


    # SteamSpy Data (tags)
    # self.tags = steamspy_data['tags']
    # self.total_reviews = steamspy_data['total_reviews']
    # self.positive_reviews = steamspy_data['total_positive']
    # self.negative_reviews = steamspy_data['total_negative']

    # Steam Reviews Data
    self.reviews = reviews_data

    # CheapShark Data
    # self.deals = cheap_shark_data

    # ITAD Data
    self.deals = itad_data['deals']
    self.tags = itad_data['tags']
    self.is_reviews = itad_data['is_reviews']
    if self.is_reviews:
      self.total_reviews = itad_data['total_reviews']
      self.positive_reviews = itad_data['total_positive']
      self.negative_reviews = itad_data['total_negative']    

    # HLTB Data
    self.hltb = hltb_data


def query_hltb(title):
  """Update HowLongToBeat data using howlongtobeatpy"""
  results_list = HowLongToBeat().search(title.lower())
  hltb_data = {}
  if results_list is not None and len(results_list) > 0:
      best_element = max(results_list, key=lambda element: element.similarity)
      hltb_data['link'] = best_element.game_web_link
      hltb_data['main'] = hltb_format(best_element.main_story)
      hltb_data['main_extra'] = hltb_format(best_element.main_extra)
      hltb_data['completionist'] = hltb_format(best_element.completionist)
      hltb_data['all_styles'] = hltb_format(best_element.all_styles)
  else: hltb_data = None

  return hltb_data

  
def query_hltb_manual(title):
    """
    Get HLTB Data without howlongtobeatpy, sometimes faster, sometimes still slow, 
    also will die if they change the key
    """
    hltb_data = {}

    ua = UserAgent()
    headers = {
            'content-type': 'application/json',
            'accept': '*/*',
            'User-Agent': ua.random.strip(),
            'referer': 'https://howlongtobeat.com/'
    }
    payload = {
        "searchType": "games",
        "searchTerms": title.split(" "),
        "searchPage": 1,
        "size": 1,
        "searchOptions": {
            "games": {
                "userId": 0,
                "platform": "",
                "sortCategory": "popular",
                "rangeCategory": "main",
                "rangeTime": {"min": 0, "max": 0},
                "gameplay": {"perspective": "", "flow": "", "genre": ""},
                "rangeYear": {"min": "", "max": ""},
                "modifier": ""
            },
            "users": {"sortCategory": "postcount"},
            "lists": {"sortCategory": "follows"},
            "filter": "",
            "sort": 0,
            "randomizer": 0
        }
    }
    res = requests.post("https://howlongtobeat.com/api/search/21fda17e4a1d49be", headers=headers, data=json.dumps(payload))
    try:
      data = res.json()['data'][0]
    except IndexError:
       return None
    
    # hltb_data['link'] = data.game_web_link
    hltb_data['main'] = hltb_format(data['comp_main'] / 3600)
    hltb_data['main_extra'] = hltb_format(data['comp_plus'] / 3600)
    hltb_data['completionist'] = hltb_format(data['comp_100'] / 3600)
    hltb_data['all_styles'] = hltb_format(data['comp_all'] / 3600)

    return hltb_data


def query_steamspy_api(steam_id):
  """Update tags using the SteamSpy API"""
  url_params = {'request': 'appdetails', 'appid':steam_id}
  res = requests.get('https://steamspy.com/api.php', params=url_params)
  app_data = res.json()

  steamspy = {
     'tags': [tag for tag in app_data['tags']],
     'total_reviews': app_data['positive'] + app_data['negative'],
     'total_positive': app_data['positive'],
     'total_negative': app_data['negative']
  }

  return steamspy


def query_cheap_shark_api(steam_id):
  """Update deals details using CheapShark API"""
  # Convert Steam App ID into CheapShark ID
  url_params = {'steamAppID':steam_id, 'limit': 1}
  res = requests.get('https://www.cheapshark.com/api/1.0/games', params=url_params)

  # Take the CheapShark ID we just got and make it a list of prices
  res = requests.get('https://www.cheapshark.com/api/1.0/games', params={'id':res.json()[0]['gameID']})
  app_deals = res.json()['deals']

  # Massive switch to remove to set storeName based on storeID (only uses active CheapShark stores which is why numbers are skipped)
  for deal in app_deals:
    match int(deal['storeID']):
      case 1:
          deal['storeName'] = "Steam"
      case 2:
          deal['storeName'] = "GamersGate"
      case 3:
          deal['storeName'] = "GreenManGaming"
      case 7:
          deal['storeName'] = "GOG"
      case 8:
          deal['storeName'] = "Origin"
      case 11:
          deal['storeName'] = "Humble Store"
      case 13:
          deal['storeName'] = "Uplay"
      case 14:
          deal['storeName'] = "IndieGameStand"
      case 15:
          deal['storeName'] = "Fanatical"
      case 21:
          deal['storeName'] = "WinGameStore"
      case 23:
          deal['storeName'] = "GameBillet"
      case 24:
          deal['storeName'] = "Voidu"
      case 25:
          deal['storeName'] = "Epic Games Store"
      case 27:
          deal['storeName'] = "Gamesplanet"
      case 28:
          deal['storeName'] = "Gamesload"
      case 29:
          deal['storeName'] = "2Game"
      case 30:
          deal['storeName'] = "IndieGala"
      case 31:
          deal['storeName'] = "Blizzard Shop"
      case 33:
          deal['storeName'] = "DLGamer"
      case 34:
          deal['storeName'] = "Noctre"
      case 35:
          deal['storeName'] = "DreamGame"
    del deal['storeID']
  
  return app_deals


def query_itad_api(steam_id, coming_soon):
  """Get prices, tags, and reviews from the ITAD API"""
  data = {}

  # Get ITAD App ID
  app_format =  'app/' + str(steam_id)
  payload = [app_format]
  res = requests.post('https://api.isthereanydeal.com/lookup/id/shop/61/v1', data=json.dumps(payload))
  app_id = res.json()[app_format]

  # Get Deals
  if not coming_soon:
    payload = [app_id]
    url_params = {
      "key": os.getenv("ITAD_API_KEY"),
      "country": "US",
      "nondeals": "true",
      "vouchers": "true"
    }
    res = requests.post('https://api.isthereanydeal.com/games/prices/v2', data=json.dumps(payload), params=url_params)
    deals = res.json()
    if len(deals) > 0: data['deals'] = deals[0]['deals']
    else: data['deals'] = None
  else: data['deals'] = None

  # Get Tags and Reviews
  url_params = {
    "key": os.getenv("ITAD_API_KEY"),
    "id": app_id
  }
  res = requests.get('https://api.isthereanydeal.com/games/info/v2', params=url_params)
  details = res.json()

  data['tags'] = details['tags']

  data['is_reviews'] = False
  for reviewer in details['reviews']:
     if reviewer['source'] == "Steam":
        total_reviews = reviewer['count']
        positive_percent = int(reviewer['score']) / 100

        data['is_reviews'] = True
        data['total_reviews'] = total_reviews
        data['total_positive'] = round(positive_percent * total_reviews)
        data['total_negative'] = total_reviews - round(positive_percent * total_reviews)

        break
  
  return data


def query_steam_api(steam_id):
  """Update game details using Steam API"""
  # Make API call
  usd = 1
  url_params = {'appids': steam_id, 'currency': usd}
  res = requests.get('https://store.steampowered.com/api/appdetails', params=url_params)
  app_details = res.json()[steam_id]['data']
  return app_details


def query_steam_reviews_api(steam_id):
  """Get Steam Reviews using Steam Reviews API"""

  # Get english reviews for display
  url_params = {
    'appids': steam_id,
    'json': 1,
    'filter': 'all',
    'language': 'english',
    'purchase_type': 'all',
    'review_type': 'all',
    'num_per_page': 10
  }
  res = requests.get(f'https://store.steampowered.com/appreviews/{steam_id}', params=url_params)
  app_reviews = res.json()
  return app_reviews['reviews']


def parse_steam_ids(data):
  """Get the display name and profile pictures for the steam ids in reviews"""
  if os.getenv('STEAM_API_KEY') is None: 
      raise ValueError('STEAM_API_KEY is not set properly in your .env file')
  
  url_params = {
    'key': os.getenv("STEAM_API_KEY"),
    'steamids': ','.join([d['author']['steamid'] for d in data])
  }
  res = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/', params=url_params)
  app_ids = res.json()['response']['players']

  for review in data:
      author = next((item for item in app_ids if item['steamid'] == review['author']['steamid']), None)
      review['author']['name'] = author['personaname']
      review['author']['profile_url'] = author['profileurl']
      review['author']['avatar'] = author['avatar']
      review['post_date'] = datetime.fromtimestamp(int(review['timestamp_created'])).strftime("%B %d %Y")
  return data


def hltb_format(num):
  """Format HowLongToBeat hours by round to the nearest half hour and adding the 1/2 symbol"""
  norm_num = round(num * 2) / 2

  if norm_num%1==0: return str(int(norm_num))
  else: return str(math.floor(norm_num)) + "½"


def soupify(requirement):
  """Formats Hardware Requirements by modifying HTML"""
  soup = BeautifulSoup(requirement, features="html.parser")
  for tag in soup.find_all("strong"):
    if tag.parent.name == "li":
      contents = tag.parent.contents[1]
      new_tag = soup.new_tag("span")
      new_tag.string = contents
      tag.parent.contents[1].replace_with(new_tag)
    elif tag.parent.name == "[document]":
      for br in soup.find_all("br"):
        br.decompose()
      for item in tag.parent.contents:
         if item.name == None and re.search("[A-Za-z]+:", item.string):
            new_tag = soup.new_tag("br")
            item.insert_after(new_tag)
      print(tag.parent.contents)

  # for tag in soup.find_all("br"):
  #   tag.decompose()
  return str(soup)


def soupificate(desc):
  """Addes header to game descriptions without a header"""
  soup = BeautifulSoup(desc, features="html.parser")
  if soup.contents[0].name != "h1":
    new_tag = soup.new_tag("h1")
    new_tag.string = "About this Game"
    soup.insert(0, new_tag)
  return str(soup)