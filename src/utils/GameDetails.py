"""The GameDetails class collects and stores game info using various APIs"""
import requests

class GameDetails :
  def __init__(self, steam_app_id):
    if isinstance(steam_app_id, str) and not steam_app_id.isdigit():
      raise ValueError("Steam App ID must be a digit")
    
    # Steam Info
    self.steam_app_id = str(steam_app_id)
    self.title = None
    self.short_description = None
    self.detailed_description = None
    self.header_img_url = None
    self.pc_requirements_min = None
    self.pc_requirements_recommended = None
    self.mac_requirements_min = None
    self.mac_requirements_recommended = None
    self.linux_requirements_min = None
    self.linux_requirements_recommended = None
    self.steam_price = None
    self.steam_discount = None
    self.is_available_windows = False
    self.is_available_mac = False
    self.is_available_linux = False
    self.screenshots = []
    self.release_date = None

    # Steam Reviews
    self.review_count = None
    self.positive_reviews = None
    self.negative_reviews = None
    self.steam_reviews = []
    
    # HowLongToBeat
    # TODO: Add HLTB data here (i'll do it soon)

    # CheapShark
    self.deals = []

    # Update with APIs
    self.update_with_steam_api()
    self.update_with_steam_reviews_api()
    self.update_with_cheap_shark_api()


  def update_with_cheap_shark_api(self):
    """Update deals details using CheapShark API"""
    # Convert Steam App ID into CheapShark ID
    url_params = {'steamAppID':self.steam_app_id, 'limit': 1}
    res = requests.get('https://www.cheapshark.com/api/1.0/games', params=url_params)

    # Take the CheapShark ID we just got and make it a list of prices
    res = requests.get('https://www.cheapshark.com/api/1.0/games', params={'id':res.json()[0]['gameID']})
    app_details = res.json()['deals']

    # Massive switch to remove to set storeName based on storeID (only uses active CheapShark stores which is why numbers are skipped)
    for deal in app_details:
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
    self.deals = app_details

   
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
    self.header_img_url = app_details['header_image']
    self.is_available_windows = app_details['platforms']['windows']
    self.is_available_mac = app_details['platforms']['mac']
    self.is_available_linux = app_details['platforms']['linux']
    if self.is_available_windows:
      if 'minimum' in app_details['pc_requirements']:
        self.pc_requirements_min = app_details['pc_requirements']['minimum']
      if 'recommended' in app_details['pc_requirements']:
        self.pc_requirements_recommended = app_details['pc_requirements']['recommended']
    if self.is_available_mac:
      if 'minimum' in app_details['mac_requirements']:
        self.mac_requirements_min = app_details['mac_requirements']['minimum']
      if 'recommended' in app_details['mac_requirements']:
        self.mac_requirements_recommended = app_details['mac_requirements']['recommended']
    if self.is_available_linux:
      if 'minimum' in app_details['linux_requirements']:
        self.linux_requirements_min = app_details['linux_requirements']['minimum']
      if 'recommended' in app_details['linux_requirements']:
        self.linux_requirements_recommended = app_details['linux_requirements']['recommended']
    if 'price_overview' in app_details:
      self.steam_price = app_details['price_overview']['final_formatted']
      self.steam_discount = app_details['price_overview']['discount_percent']
    self.screenshots = [screenshot['path_full'] for screenshot in app_details['screenshots']]
    self.release_date = app_details['release_date']['date']

  def update_with_steam_reviews_api(self):
    url_params = {
      'appids': self.steam_app_id,
      'json': 1,
      'filter': 'all',
      'language': 'english',
      'purchase_type': 'all',
      'review_type': 'all',
      'num_per_page': 5
      }
    res = requests.get(f'https://store.steampowered.com/appreviews/{self.steam_app_id}', params=url_params)
    app_reviews = res.json()
    self.review_count = app_reviews['query_summary']['total_reviews']
    self.positive_reviews = app_reviews['query_summary']['total_positive']
    self.negative_reviews = app_reviews['query_summary']['total_negative']
    self.steam_reviews = app_reviews['reviews']