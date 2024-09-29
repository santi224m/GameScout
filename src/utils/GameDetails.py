"""The GameDetails class collects and stores game info using various APIs"""
import requests
import math
import os
from howlongtobeatpy import HowLongToBeat
from dotenv import load_dotenv
import time

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
    self.metacritic = {
      'score': None,
      'url': None
    }
    self.legal_notice = None;
    self.categories = []
    self.screenshots = []
    self.achievements = None
    self.release_date = None
    self.esrb_rating = None

    # Steam Spy
    self.tags = []

    # Steam Reviews
    self.total_reviews = None
    self.positive_reviews = None
    self.negative_reviews = None
    self.steam_reviews = []
    
    # HowLongToBeat
    self.hltb = {
      'link': None,
      'main': None,
      'main_extra': None,
      'completionist': None,
      'all_styles': None
    }

    # CheapShark
    self.deals = []

    init_end = time.perf_counter()

    steam_data = query_steam_api(self.steam_app_id)
    steam_end = time.perf_counter()

    tags = query_steamspy_api(self.steam_app_id)
    tags_end = time.perf_counter()

    reviews_data = query_steam_reviews_api(self.steam_app_id)
    reviews_end = time.perf_counter()

    parse_steam_ids(reviews_data)
    parse_reviews_end = time.perf_counter()

    cheap_shark_data = query_cheap_shark_api(self.steam_app_id)
    cheapshark_end = time.perf_counter()

    hltb_data = query_hltb(steam_data['name'])
    hltb_end = time.perf_counter()

    self.update(steam_data, tags, reviews_data, cheap_shark_data, hltb_data)
    update_end = time.perf_counter()

    print(f"Init variables in {init_end - start:0.4f} seconds")
    print(f"Gathered Steam Data in {steam_end - init_end:0.4f} seconds")
    print(f"Gathered Tags Data in {tags_end - steam_end:0.4f} seconds")
    print(f"Gathered Reviews Data in {reviews_end - tags_end:0.4f} seconds")
    print(f"Updated Reviews Data in {parse_reviews_end - reviews_end:0.4f} seconds")
    print(f"Gathered CheapShark Data in {cheapshark_end - parse_reviews_end:0.4f} seconds")
    print(f"Gathered HLTB in {hltb_end - cheapshark_end:0.4f} seconds")
    print(f"Update variables in {update_end - hltb_end:0.4f} seconds")
    print(f"Total Time: {update_end - start:0.4f} seconds")

  def update(self, steam_data, tags, reviews_data, cheap_shark_data, hltb_data):
    """Update GameDetails with data from our various API's"""

    # Steam
    self.title = steam_data['name']
    self.short_description = steam_data['short_description']
    self.detailed_description = steam_data['detailed_description']
    self.header_img = steam_data['header_image']
    self.developers = ', '.join(steam_data['developers'])
    self.publishers = ', '.join(steam_data['publishers'])
    self.platforms = steam_data['platforms']
    if self.platforms['windows']:
      self.pc_requirements = steam_data['pc_requirements']
    if self.platforms['mac']:
      self.mac_requirements = steam_data['mac_requirements']
    if self.platforms['linux']:
      self.linux_requirements = steam_data['linux_requirements']
    if 'legal_notice' in steam_data:
       self.legal_notice = steam_data['legal_notice']
    if 'metacritic' in steam_data:
      self.metacritic = steam_data['metacritic']
    self.categories = steam_data['categories']
    self.screenshots = steam_data['screenshots']
    if 'achievements' in steam_data:
       self.achievements = steam_data['achievements']
    self.release_date = steam_data['release_date']['date']
    if 'ratings' in steam_data and 'esrb' in steam_data['ratings']:
       self.esrb_rating = steam_data['ratings']['esrb']

    # SteamSpy Data (tags)
    self.tags = tags

    # Steam Reviews Data
    self.total_reviews = reviews_data['total_reviews']
    self.positive_reviews = reviews_data['total_positive']
    self.negative_reviews = reviews_data['total_negative']
    self.steam_reviews = reviews_data['reviews']

    # CheapShark Data
    self.deals = cheap_shark_data

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


def query_steamspy_api(steam_id):
  """Update tags using the SteamSpy API"""
  url_params = {'request': 'appdetails', 'appid':steam_id}
  res = requests.get('https://steamspy.com/api.php', params=url_params)
  app_tags = res.json()['tags']

  return [tag for tag in app_tags]


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
  # Get total review numbers by doing all languanges
  url_params = {
    'appids': steam_id,
    'json': 1,
    'filter': 'all',
    'language': 'all',
    'purchase_type': 'all',
    'review_type': 'all',
    'num_per_page': 1
  }
  res = requests.get(f'https://store.steampowered.com/appreviews/{steam_id}', params=url_params)
  app_reviews = res.json()['query_summary']

  data = {}
  data['total_reviews'] = app_reviews['total_reviews']
  data['total_positive'] = app_reviews['total_positive']
  data['total_negative'] = app_reviews['total_negative']

  # Get only english reviews for display
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
  
  data['reviews'] = app_reviews['reviews']

  return data


def parse_steam_ids(data):
  """Get the display name and profile pictures for the steam ids in reviews"""
  if os.getenv('STEAM_API_KEY') is None: 
      raise ValueError('STEAM_API_KEY is not set properly in your .env file')
  
  url_params = {
    'key': os.getenv("STEAM_API_KEY"),
    'steamids': ','.join([d['author']['steamid'] for d in data['reviews']])
  }
  res = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/', params=url_params)
  app_ids = res.json()['response']['players']

  for review in data['reviews']:
      author = next((item for item in app_ids if item['steamid'] == review['author']['steamid']), None)
      review['author']['name'] = author['personaname']
      review['author']['profile_url'] = author['profileurl']
      review['author']['avatar'] = author['avatar']


def hltb_format(num):
  """Format HowLongToBeat hours by round to the nearest half hour and adding the 1/2 symbol"""
  norm_num = round(num * 2) / 2

  if norm_num%1==0: return str(int(norm_num))
  else: return str(math.floor(norm_num)) + "½"