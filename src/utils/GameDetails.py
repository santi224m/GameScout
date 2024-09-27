"""The GameDetails class collects and stores game info using various APIs"""
import requests
import math
import os
from howlongtobeatpy import HowLongToBeat
from dotenv import load_dotenv

load_dotenv()

class GameDetails :
  def __init__(self, steam_app_id):
    if isinstance(steam_app_id, str) and not steam_app_id.isdigit():
      raise ValueError("Steam App ID must be a digit")
    
    # Steam Info
    self.steam_app_id = str(steam_app_id)
    self.title = None
    self.short_description = None
    self.detailed_description = None
    self.header_img = None
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
    self.categories = []
    self.screenshots = []
    self.achievements = None
    self.release_date = None
    self.esrb_rating = None

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

    # Update with APIs
    self.update_with_steam_api()
    self.update_with_steam_reviews_api()
    self.update_with_hltb()
    self.update_with_cheap_shark_api()

  def update_with_hltb(self):
    """Update HowLongToBeat data using howlongtobeatpy"""
    results_list = HowLongToBeat().search(self.title.lower())
    if results_list is not None and len(results_list) > 0:
        best_element = max(results_list, key=lambda element: element.similarity)
        self.hltb['link'] = best_element.game_web_link
        self.hltb['main'] = hltb_format(best_element.main_story)
        self.hltb['main_extra'] = hltb_format(best_element.main_extra)
        self.hltb['completionist'] = hltb_format(best_element.completionist)
        self.hltb['all_styles'] = hltb_format(best_element.all_styles)
    else: self.hltb = None


  def update_with_cheap_shark_api(self):
    """Update deals details using CheapShark API"""
    # Convert Steam App ID into CheapShark ID
    url_params = {'steamAppID':self.steam_app_id, 'limit': 1}
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
    
    # Update Deals
    self.deals = app_deals

   
  def update_with_steam_api(self):
    """Update game details using Steam API"""
    # Make API call
    usd = 1
    url_params = {'appids': self.steam_app_id, 'currency': usd}
    res = requests.get('https://store.steampowered.com/api/appdetails', params=url_params)
    app_details = res.json()[self.steam_app_id]['data']

    # Update game details
    self.title = app_details['name']
    self.short_description = app_details['short_description']
    self.detailed_description = app_details['detailed_description']
    self.header_img = app_details['header_image']
    self.platforms = app_details['platforms']
    if self.platforms['windows']:
      self.pc_requirements = app_details['pc_requirements']
    if self.platforms['mac']:
      self.mac_requirements = app_details['mac_requirements']
    if self.platforms['linux']:
      self.linux_requirements = app_details['linux_requirements']
    if 'metacritic' in app_details:
      self.metacritic = app_details['metacritic']
    self.categories = app_details['categories']
    self.screenshots = app_details['screenshots']
    if 'achievements' in app_details:
       self.achievements = app_details['achievements']
    self.release_date = app_details['release_date']['date']
    if 'ratings' in app_details and 'esrb' in app_details['ratings']:
       self.esrb_rating = app_details['ratings']['esrb']

  def update_with_steam_reviews_api(self):
    # Get total review numbers by doing all languanges
    url_params = {
      'appids': self.steam_app_id,
      'json': 1,
      'filter': 'all',
      'language': 'all',
      'purchase_type': 'all',
      'review_type': 'all',
      'num_per_page': 1
    }
    res = requests.get(f'https://store.steampowered.com/appreviews/{self.steam_app_id}', params=url_params)
    app_reviews = res.json()['query_summary']

    self.total_reviews = app_reviews['total_reviews']
    self.positive_reviews = app_reviews['total_positive']
    self.negative_reviews = app_reviews['total_negative']

    # Get only english reviews for display
    url_params = {
      'appids': self.steam_app_id,
      'json': 1,
      'filter': 'all',
      'language': 'english',
      'purchase_type': 'all',
      'review_type': 'all',
      'num_per_page': 10
    }
    res = requests.get(f'https://store.steampowered.com/appreviews/{self.steam_app_id}', params=url_params)
    app_reviews = res.json()
    
    self.steam_reviews = app_reviews['reviews']
    
    self.parse_steam_ids()

  def parse_steam_ids(self):
    """Get the display name and profile pictures for the steam ids in reviews"""
    if os.getenv('STEAM_API_KEY') is None: 
       raise ValueError('STEAM_API_KEY is not set properly in your .env file')
    
    url_params = {
      'key': os.getenv("STEAM_API_KEY"),
      'steamids': ','.join([d['author']['steamid'] for d in self.steam_reviews])
    }
    print(url_params['steamids'])
    res = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/', params=url_params)
    app_ids = res.json()['response']['players']

    for review in self.steam_reviews:
       author = next((item for item in app_ids if item['steamid'] == review['author']['steamid']), None)
       review['author']['name'] = author['personaname']
       review['author']['profile_url'] = author['profileurl']
       review['author']['avatar'] = author['avatar']


def hltb_format(num):
  """Format HowLongToBeat hours by round to the nearest half hour and adding the 1/2 symbol"""
  norm_num = round(num * 2) / 2

  if norm_num%1==0: return str(int(norm_num))
  else: return str(math.floor(norm_num)) + "½"