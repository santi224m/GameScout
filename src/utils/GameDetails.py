"""The GameDetails class collects and stores game info using various APIs"""
import json
import logging
import multiprocessing
import os
import pickle
import re
import requests
import threading
import time
import bbcode
from datetime import datetime

import redis
from bs4 import BeautifulSoup
from flask import abort

from src.utils.HLTBHelper import HLTB
from src.utils.db_utils import db_utils
from src.utils.BBParser import BBParser

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO)

class GameDetails :
  def __init__(self, steam_app_id):
    start = time.perf_counter()

    if isinstance(steam_app_id, str) and not steam_app_id.isdigit():
      raise ValueError("Steam App ID must be a digit")

    # Threading condition variable
    self.cv_itad_id = threading.Condition()
    self.cv_steam_reviews = threading.Condition()
    self.cv_steam_api = threading.Condition()

    # Steam Info
    self.steam_app_id = str(steam_app_id)
    self.itad_app_id = None
    self.title = None
    self.short_description = None
    self.detailed_description = None
    self.header_img = None
    self.library_img = None
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
      'main': None,
      'main_extra': None,
      'completionist': None,
      'all_styles': None
    }

    # Redis game cache
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    # See if the Steam ID is already in Redis
    if (game_cache := redis_conn.get(steam_app_id)) is not None:
      logging.info(f"{str(steam_app_id):<9} - - Using game cache...")
      game = pickle.loads(game_cache)
      self.__dict__ = game.__dict__.copy()  # Set self to game cache
    else:
      # If not in Redis, get it the old fashioned way
      self.steam_api_res = None
      self.steam_reviews_api_res = None
      self.ITAD_api_2_res = None
      self.ITAD_api_3_res = None
      self.steamplayers_api_res = None
      self.hltb_data = None

      exists = self.call_apis_w_threads()

      if exists is False: return None

      steam_data = query_steam_api(self.steam_app_id, self.steam_api_res)

      reviews_data = query_steam_reviews_api(self.steam_reviews_api_res)

      reviews_data = parse_steam_ids(reviews_data, self.steamplayers_api_res)

      itad_data = query_itad_api(self.steam_app_id, steam_data['release_date']['coming_soon'], self.ITAD_api_2_res, self.ITAD_api_3_res)

      self.update(steam_data, reviews_data, itad_data, self.hltb_data)
      update_end = time.perf_counter()

      logging.info(f"{str(steam_app_id):<9} - - Total Time: {update_end - start:0.4f} seconds")

      # Store game_details in Redis cache
      game_cache = pickle.dumps(self)
      redis_conn.set(steam_app_id, game_cache)
      HOUR_SECONDS = 3600
      redis_conn.expire(steam_app_id, HOUR_SECONDS)

  def call_apis_w_threads(self):
    """Make all api calls using threads to reduce wait time"""
    start = time.perf_counter()
    thread_get_ITAD_ID = threading.Thread(target=self.get_ITAD_ID)
    thread_get_ITAD_ID.start()
    thread_steamapi = threading.Thread(target=self.get_steamapi)
    thread_steamapi.start()
    thread_steamreviewsapi = threading.Thread(target=self.get_steam_reviews_api)
    thread_steamreviewsapi.start()
    valid_id = True
    with self.cv_steam_reviews:
      while self.steam_reviews_api_res is None:
        pass
      if ('data' not in self.steam_api_res.json()[self.steam_app_id]): return False
    thread_ITAD_api_2 = threading.Thread(target=self.get_ITAD_api_2)
    thread_ITAD_api_2.start()
    thread_ITAD_api_3 = threading.Thread(target=self.get_ITAD_api_3)
    thread_ITAD_api_3.start()
    thread_steamplayers_api = threading.Thread(target=self.get_steamplayers_api)
    thread_steamplayers_api.start()
    q = multiprocessing.Queue()
    thread_steamapi.join()
    hltb_proc = multiprocessing.Process(target=get_htlb_data, args=(q, self.steam_api_res.json()[self.steam_app_id]['data']['name'], self.steam_app_id))
    hltb_proc.start()

    # Wait for all threads
    thread_get_ITAD_ID.join()
    thread_steamreviewsapi.join()
    thread_ITAD_api_2.join()
    thread_ITAD_api_3.join()
    thread_steamplayers_api.join()
    hltb_proc.join()
    self.hltb_data = q.get()
    # Cannot cache locks; Reset to None
    self.cv_itad_id = None
    self.cv_steam_reviews = None
    self.cv_steam_api = None
    end = time.perf_counter()
    logging.info(f"{str(self.steam_app_id):<9} - - call_apis_w_threads: Total time {end - start:0.4f} seconds")

  def get_steamapi(self):
    start = time.perf_counter()
    usd = 1
    url_params = {'appids': self.steam_app_id, 'currency': usd}
    self.steam_api_res = requests.get('https://store.steampowered.com/api/appdetails', params=url_params)
    with self.cv_steam_api:
      self.cv_steam_api.notify_all()
    end = time.perf_counter()
    logging.info(f"{str(self.steam_app_id):<9} - - SteamAPI: Total time {end - start:0.4f} seconds")

  def get_steam_reviews_api(self):
    start = time.perf_counter()
    url_params = {
      'appids': self.steam_app_id,
      'json': 1,
      'filter': 'all',
      'language': 'english',
      'purchase_type': 'all',
      'review_type': 'all',
      'num_per_page': 10
    }
    self.steam_reviews_api_res = requests.get(f'https://store.steampowered.com/appreviews/{self.steam_app_id}', params=url_params)
    with self.cv_steam_reviews:
      self.cv_steam_reviews.notify_all()
    end = time.perf_counter()
    logging.info(f"{str(self.steam_app_id):<9} - - SteamReviewAPI: Total time {end - start:0.4f} seconds")

  def get_ITAD_ID(self):
    start = time.perf_counter()
    if (itad_app_id := db_utils.get_itad_game_id(self.steam_app_id)):
      self.itad_app_id = itad_app_id
    else:
      key =  'app/' + str(self.steam_app_id)
      payload = [key]
      res = requests.post('https://api.isthereanydeal.com/lookup/id/shop/61/v1', data=json.dumps(payload))
      self.itad_app_id = res.json()[key]
      db_utils.insert_itad_game_id(self.steam_app_id, self.itad_app_id)
    with self.cv_itad_id:
      self.cv_itad_id.notify_all()
    end = time.perf_counter()
    logging.info(f"{str(self.steam_app_id):<9} - - ITADapi1: Total time {end - start:0.4f} seconds")

  def get_ITAD_api_2(self):
    start = time.perf_counter()

    with self.cv_itad_id:
      while self.itad_app_id is None:
        self.cv_itad_id.wait()

    app_format =  'app/' + str(self.steam_app_id)
    payload = [app_format]
    with self.cv_steam_api:
      while self.steam_api_res is None:
        self.cv_steam_api.wait()
    coming_soon = self.steam_api_res.json()[self.steam_app_id]['data']['release_date']['coming_soon']
    # Get Deals
    if not coming_soon:
      payload = [self.itad_app_id]
      url_params = {
        "key": os.getenv("ITAD_API_KEY"),
        "country": "US",
        "nondeals": "true",
        "vouchers": "true"
      }
      self.ITAD_api_2_res = requests.post('https://api.isthereanydeal.com/games/prices/v2', data=json.dumps(payload), params=url_params)
    end = time.perf_counter()
    logging.info(f"{str(self.steam_app_id):<9} - - ITADapi2: Total time {end - start:0.4f} seconds")

  def get_ITAD_api_3(self):
    start = time.perf_counter()

    with self.cv_itad_id:
      while self.itad_app_id is None:
        self.cv_itad_id.wait()

    url_params = {
      "key": os.getenv("ITAD_API_KEY"),
      "id": self.itad_app_id
    }
    self.ITAD_api_3_res = requests.get('https://api.isthereanydeal.com/games/info/v2', params=url_params)
    end = time.perf_counter()
    logging.info(f"{str(self.steam_app_id):<9} - - ITADapi3: Total time {end - start:0.4f} seconds")

  def get_steamplayers_api(self):
    start = time.perf_counter()

    with self.cv_steam_reviews:
      while self.steam_reviews_api_res is None:
        self.cv_steam_reviews.wait()
    data = self.steam_reviews_api_res.json()['reviews']
    url_params = {
      'key': os.getenv("STEAM_API_KEY"),
      'steamids': ','.join([d['author']['steamid'] for d in data])
    }
    self.steamplayers_api_res = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/', params=url_params)

    end = time.perf_counter()
    logging.info(f"{str(self.steam_app_id):<9} - - SteamPlayersAPI: Total time {end - start:0.4f} seconds")

  def update(self, steam_data, reviews_data, itad_data, hltb_data):
    """Update GameDetails with data from our various API's"""

    # Steam
    self.title = steam_data['name']
    self.short_description = steam_data['short_description']
    self.detailed_description = soupificate(steam_data['detailed_description'])
    self.header_img = steam_data['header_image']
    self.library_img = f"https://steamcdn-a.akamaihd.net/steam/apps/{self.steam_app_id}/library_600x900_2x.jpg"
    if 'developers' in steam_data and len(steam_data['developers']) > 0:
      self.developers = ', '.join(steam_data['developers'])
    if 'developers' in steam_data and len(steam_data['publishers']) > 0:
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
    if 'screenshots' in steam_data:
      self.screenshots = steam_data['screenshots']
    if 'achievements' in steam_data:
      self.achievements = steam_data['achievements']
    self.release_date = steam_data['release_date']
    if steam_data['ratings'] and 'esrb' in steam_data['ratings']:
      self.esrb_rating = steam_data['ratings']['esrb']
      if 'interactive_elements' not in self.esrb_rating:
        self.esrb_rating['interactive_elements'] = None
      else: self.esrb_rating['interactive_elements'] = self.esrb_rating['interactive_elements'].replace("\n", "<br>")
      if 'descriptors' not in self.esrb_rating:
        self.esrb_rating['descriptors'] = None
      else: self.esrb_rating['descriptors'] = self.esrb_rating['descriptors'].replace("\n", "<br>")

    # Steam Reviews Data
    self.reviews = reviews_data

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

def get_htlb_data(q, name, id):
  start = time.perf_counter()
  hltb_data = HLTB.search(name)
  q.put(hltb_data)
  end = time.perf_counter()
  logging.info(f"{str(id):<9} - - HLTB Helper: Total time {end - start:0.4f} seconds")

def query_itad_api(steam_id, coming_soon, ITAD_api_2_res, ITAD_api_3_res):
  """Get prices, tags, and reviews from the ITAD API"""
  data = {}

  # Get ITAD App ID
  app_format =  'app/' + str(steam_id)

  # Get Deals
  if not coming_soon:
    deals = ITAD_api_2_res.json()
    if len(deals) > 0: data['deals'] = deals[0]['deals']
    else: data['deals'] = None
  else: data['deals'] = None

  res = ITAD_api_3_res
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

def query_steam_api(steam_id, steam_api_res):
  """Update game details using Steam API"""
  res = steam_api_res
  if not 'data' in res.json()[steam_id]: abort(400) # Abort if no steam data
  app_details = res.json()[steam_id]['data']

  features = {
    "1": '<i class="fa-solid fa-user-group"></i>',                                          # Multiplayer < Cross Platform Multiplayer || Online PvP || Online Co-op
    "2": '<i class="fa-solid fa-user"></i>',                                                # Single Player
    "8": '<i class="fa-solid fa-shield-halved"></i>',                                       # Valve Anti-Cheat enabled
    "9": '<i class="fa-solid fa-user-group"></i>',                                          # Co-op < Online Co-op
    "13": '<i class="fa-solid fa-closed-captioning"></i>',                                  # Captions Available
    "14": '<i class="fa-solid fa-comment"></i>',                                            # Commentary Available
    "15": '<i class="fa-solid fa-chart-simple"></i>',                                       # Stats
    "16": '<i class="fa-solid fa-screwdriver-wrench"></i>',                                 # Includes Source SDK
    "17": '<i class="fa-solid fa-file-pen"></i>',                                           # Includes Level Editor
    "18": '<img src="/static/img/controller_blue.svg" class="icon" alt="Controller Icon">', # Partial Controller Support
    "20": '<i class="fa-solid fa-user-group"></i>',                                         # MMO
    "22": '<i class="fa-solid fa-award"></i>',                                              # Steam Achievements
    "23": '<i class="fa-solid fa-cloud"></i>',                                              # Steam Cloud
    "24": '<i class="fa-solid fa-user-group"></i>',                                         # Shared / Split Screen < Shared / Split Screen Co-op || Shared / Split Screen PvP
    "25": '<i class="fa-solid fa-list-ol"></i>',                                            # Steam Leaderboards
    "27": '<i class="fa-solid fa-user-group"></i>',                                         # Cross Platform Multiplayer
    "28": '<img src="/static/img/controller_blue.svg" class="icon" alt="Controller Icon">', # Full Controller Support
    "29": '<img src="/static/img/cards.svg" class="icon" alt="Cards Icon">',                # Steam Trading Cards
    "30": '<i class="fa-solid fa-hammer"></i>',                                             # Steam Workshop
    "35": '<i class="fa-solid fa-cart-shopping"></i>',                                      # In App Purchases
    "36": '<i class="fa-solid fa-user-group"></i>',                                         # Online PvP
    "37": '<i class="fa-solid fa-user-group"></i>',                                         # Shared / Split Screen PvP
    "38": '<i class="fa-solid fa-user-group"></i>',                                         # Online Co-op
    "39": '<i class="fa-solid fa-user-group"></i>',                                         # Shared / Split Screen Co-op
    "41": '<i class="fa-brands fa-chromecast"></i>',                                        # Remote Play on Phone
    "42": '<i class="fa-brands fa-chromecast"></i>',                                        # Remote Play on Tablet
    "43": '<i class="fa-brands fa-chromecast"></i>',                                        # Remote Play on TV
    "44": '<i class="fa-solid fa-wifi"></i>',                                               # Remote Play on Together
    "47": '<i class="fa-solid fa-user-group"></i>',                                         # LAN PvP
    "48": '<i class="fa-solid fa-user-group"></i>',                                         # LAN Co-op
    "49": '<i class="fa-solid fa-user-group"></i>',                                         # PVP < LAN PvP < Online PvP
    "51": '<i class="fa-solid fa-hammer"></i>',                                             # Steam Workshop (Not Used?)
    "52": '<i class="fa-solid fa-wand-magic"></i>',                                         # Tracked Controller Support
    "53": '<i class="fa-solid fa-vr-cardboard"></i>',                                       # VR Supported
    "61": '<i class="fa-solid fa-desktop"></i>',                                            # HDR Available
    "62": '<i class="fa-solid fa-users"></i>',                                              # Family Sharing
    "63": '<i class="fa-solid fa-location-dot"></i>',                                       # Steam Timeline
    "e": '<i class="fa-solid fa-xmark"></i>'
  }

  if 'categories' in app_details:
    categories = app_details['categories']

  # If CPM del M
  if find(categories, 1) is not None and find(categories, 27):
    del categories[find(categories, 1)]
  # If Online Co-op del Co-op
  if find(categories, 9) and find(categories, 38):
    del(categories[find(categories, 9)])
  # If SSS Co-op or SSS PvP del SSS
  if find(categories, 24) and (find(categories, 37) or find(categories, 39)):
    del(categories[find(categories, 24)])
  # If LAN PvP del PVP
  if find(categories, 49) and find(categories, 47):
    del(categories[find(categories, 49)])
  # If Online PvP del LAN PvP and PvP
  if find(categories, 36) and (find(categories, 47) or find(categories, 49)):
    if find(categories, 47): del(categories[find(categories, 47)])
    if find(categories, 49): del(categories[find(categories, 49)])
  # If Online PvP del M
  if find(categories, 36) and find(categories, 1) is not None:
    del(categories[find(categories, 1)])
  # If Online Co-op del M
  if find(categories, 38) and find(categories, 1) is not None:
    del(categories[find(categories, 1)])
  # If there are 2 steam workshops, del one
  if find(categories, 30) and find(categories, 51):
    del(categories[find(categories, 51)])

  for category in categories:
    if str(category['id']) in features: 
      category['icon'] = features[str(category['id'])]
    else: category['icon'] = features['e']
     
  app_details['categories'] = categories
  return app_details

def query_steam_reviews_api(steam_reviews_api_res):
  """Get Steam Reviews using Steam Reviews API"""
  bbcode_test = """
  [h1] Heading 1 [/h1]
  [h2] Heading 2 [/h2]
  [h3] Heading 3 [/h3]
  [b] Bold text [/b]
  [u] Underlined text [/u]
  [i] Italic text [/i]
  [strike] Strikethrough text [/strike]
  [spoiler] Spoiler text [/spoiler]
  hr below this
  [hr][/hr]
  hr above this
  [url=store.steampowered.com] Website link [/url]
  [list]
  [*] Bulleted list
  [*] Bulleted list
  [*] Bulleted list
  [/list]
  [olist]
  [*] Ordered list
  [*] Ordered list
  [*] Ordered list
  [/olist]
  [quote=author;3155312274947358220] Quoted text [/quote]
  [code] Fixed-width font,              preserves spaces [/code]
  [noparse][b]Hello![/b][/noparse]
  [table]
    [tr]
      [th] Name [/th]
      [th] Age [/th]
    [/tr]
    [tr]
      [td] John [/td]
      [td] 65 [/td]
    [/tr]
    [tr]
      [td] Gitte [/td]
      [td] 40 [/td]
    [/tr]
    [tr]
      [td] Sussie [/td]
      [td] 19 [/td]
    [/tr]
  [/table]
  """
  # Get english reviews for display
  res = steam_reviews_api_res
  app_reviews = res.json()['reviews']
  # Uncomment to use test review
  # app_reviews[0]['review'] = bbcode_test

  for review in app_reviews:
    review['review'] = BBParser().format_text(review['review'])

  return app_reviews

def parse_steam_ids(data, steamplayers_api_res):
  """Get the display name and profile pictures for the steam ids in reviews"""
  if os.getenv('STEAM_API_KEY') is None: 
      raise ValueError('STEAM_API_KEY is not set properly in your .env file')
  
  url_params = {
    'key': os.getenv("STEAM_API_KEY"),
    'steamids': ','.join([d['author']['steamid'] for d in data])
  }
  app_ids = steamplayers_api_res.json()['response']['players']

  for review in data:
      author = next((item for item in app_ids if item['steamid'] == review['author']['steamid']), None)
      review['author']['name'] = author['personaname']
      review['author']['profile_url'] = author['profileurl']
      review['author']['avatar'] = author['avatar']
      review['post_date'] = datetime.fromtimestamp(int(review['timestamp_created'])).strftime("%B %d %Y")
  return data

def soupify(requirement):
  """Formats Hardware Requirements by modifying HTML"""
  soup = BeautifulSoup(requirement, features="html.parser")
  for tag in soup.find_all("strong"):
    if tag.parent.name == "li" and tag.parent.contents[1].name == None and tag.contents[0] != "Additional Notes":
      contents = tag.parent.contents[1]
      new_tag = soup.new_tag("span")
      new_tag.string = contents
      tag.parent.contents[1].replace_with(new_tag)
    elif tag.parent.name == "li" and tag.contents[0] == "Additional Notes":
      wrapper = soup.new_tag("li")
      header = soup.new_tag("strong")
      header.string = tag.contents[0]
      wrapper.append(header)
      new_tag = soup.new_tag("span")

      new_tag.append(tag.parent)
      new_tag.li.unwrap()
      new_tag.contents[0].decompose()

      wrapper.append(new_tag)
      soup.ul.append(wrapper)
    elif tag.parent.name == "[document]":
      for br in soup.find_all("br"):
        br.decompose()
      for item in tag.parent.contents:
         if item.name == None and re.search("[A-Za-z]+:", item.string):
            new_tag = soup.new_tag("br")
            item.insert_after(new_tag)
  return str(soup)

def soupificate(desc):
  """Addes header to game descriptions without a header"""
  soup = BeautifulSoup(desc, features="html.parser")
  if len(soup.contents) > 0 and soup.contents[0].name != "h1":
    new_tag = soup.new_tag("h1")
    new_tag.string = "About this Game"
    soup.insert(0, new_tag)
  return str(soup)

def find(categories, id):
   return next((i for i, item in enumerate(categories) if str(item["id"]) == str(id)), None)