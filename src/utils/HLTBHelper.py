import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import re
import time
import math
import redis
import pickle

base_url = "https://howlongtobeat.com/"
search_url = base_url + "api/search/"

class HLTB:
  def __init__(self, title): 
    self.data = self.get_game_data(title)

    if self.data:
      self.main = hltb_format(self.data['comp_main'])
      self.main_extra = hltb_format(self.data['comp_plus'])
      self.all = hltb_format(self.data['comp_all'])
      self.completionist = hltb_format(self.data['comp_100'])

  def get_payload(self, title):
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
    return json.dumps(payload)

  def get_key(self):
    # Connect to Redis
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    # See if the HLTB key is already in Redis
    if (key_cache := redis_conn.get("hltb_key")) is not None:
      print("Using key cache...")
      return pickle.loads(key_cache)
    else:
      headers = self.get_headers()
      resp = requests.get(base_url, headers=headers)
      if resp.status_code == 200 and resp.text is not None:
        soup = BeautifulSoup(resp.text, 'html.parser')
        scripts = soup.find_all('script', src=True)
        matching_scripts = [script['src'] for script in scripts if '_app-' in script['src']]
        for script_url in matching_scripts:
            script_url = base_url + script_url
            script_resp = requests.get(script_url, headers=headers)
            if script_resp.status_code == 200 and script_resp.text is not None:
                pattern = r'"/api/search/".concat\("([a-zA-Z0-9]+)"\)'
                matches = re.findall(pattern, script_resp.text)
                for match in matches:
                  # Store game_details in Redis cache
                  key_cache = pickle.dumps(match)
                  redis_conn.set("hltb_key", key_cache)
                  HOUR_SECONDS = 86400
                  redis_conn.expire("hltb_key", HOUR_SECONDS)
                  return match
      return None

  def get_headers(self):
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random.strip(),
        "referer": base_url,
        "Accepts": "*/*",
        "Content-Type": "application/json"
    }
    return headers

  def get_game_data(self, title):
    headers = self.get_headers()
    payload = self.get_payload(title)
    url = search_url + self.get_key()

    res = requests.post(url, headers=headers, data=payload)
    try:
      return res.json()['data'][0]
    except IndexError:
      return None
  
  def package(self):
    if self.data: return {
      'main': self.main,
      'main_extra': self.main_extra,
      'completionist': self.all,
      'all_styles': self.completionist
    }
    else: return None

def hltb_format(num):
  """Format HowLongToBeat hours by round to the nearest half hour and adding the 1/2 symbol"""
  num_hours = num / 3600
  norm_num = round(num_hours * 2) / 2

  if norm_num%1==0: return str(int(norm_num))
  else: return str(math.floor(norm_num)) + "½"
