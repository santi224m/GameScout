import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import re
import time
import math
import redis
import pickle

class HLTB:
  BASE_URL = "https://howlongtobeat.com/"
  SEARCH_URL = BASE_URL + "api/find/"
  GAME_URL = BASE_URL + "game/"

  def search(title: str) -> dict:
    if title is None or len(title) == 0: return None

    res = HLTB.search_game(title)

    if res is not None: return HLTB.package(res)

  def get_payload(title: str, api_key: str=None) -> str:
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
          "rangeTime": {
            "min": 0,
            "max": 0
          },
          "gameplay": {
            "perspective": "",
            "flow": "",
            "genre": "",
            "difficulty": ""
          },
          "rangeYear": {
            "min": "",
            "max": ""
          },
          "modifier": ""
        },
        "users": {
          "sortCategory": "postcount"
        },
        "lists": {
          "sortCategory": "follows"
        },
        "filter": "",
        "sort": 0,
        "randomizer": 0
      }
    }

    if api_key is not None: payload['searchOptions']['users']['id'] = api_key
  
    return json.dumps(payload)

  def get_key() -> str:
    # Connect to Redis
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    # See if the HLTB key is already in Redis
    if (key_cache := redis_conn.get("hltb_key")) is not None:
      return pickle.loads(key_cache)
    else:
      headers = HLTB.get_headers()
      resp = requests.get(HLTB.BASE_URL, headers=headers)
      if resp.status_code == 200 and resp.text is not None:
        soup = BeautifulSoup(resp.text, 'html.parser')
        scripts = soup.find_all('script', src=True)
        matching_scripts = [script['src'] for script in scripts if '_app-' in script['src']]
        for script_url in matching_scripts:
            script_url = HLTB.BASE_URL + script_url
            script_resp = requests.get(script_url, headers=headers)
            if script_resp.status_code == 200 and script_resp.text is not None:
                pattern = r'\/api\/find\/"(?:\.concat\("[^"]*"\))*'
                matches = re.findall(pattern, script_resp.text)
                if matches:
                  matches = str(matches).split('.concat')
                  matches = [re.sub(r'["\(\)\[\]\']', '', match) for match in matches[1:]]
                  key = ''.join(matches)
                  key_cache = pickle.dumps(key)
                  redis_conn.set("hltb_key", key_cache)
                  HOUR_SECONDS = 86400
                  redis_conn.expire("hltb_key", HOUR_SECONDS)
                  return key
      return None

  def get_id() -> str:
    # Connect to Redis
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    # See if the HLTB key is already in Redis
    if (key_cache := redis_conn.get("hltb_id")) is not None:
      return pickle.loads(key_cache)
    else:
      headers = HLTB.get_headers()
      resp = requests.get(HLTB.BASE_URL, headers=headers)
      if resp.status_code == 200 and resp.text is not None:
        soup = BeautifulSoup(resp.text, 'html.parser')
        scripts = soup.find_all('script', src=True)
        matching_scripts = [script['src'] for script in scripts if '_app-' in script['src']]
        for script_url in matching_scripts:
            script_url = HLTB.BASE_URL + script_url
            script_resp = requests.get(script_url, headers=headers)
            if script_resp.status_code == 200 and script_resp.text is not None:
                pattern = r'users:\{id:"([^"]+)"'
                match = re.search(pattern, script_resp.text)
                if match:
                    user_id = match.group(1)
                    id_cache = pickle.dumps(user_id)
                    redis_conn.set("hltb_id", id_cache)
                    HOUR_SECONDS = 86400
                    redis_conn.expire("hltb_id", HOUR_SECONDS)
                    return user_id
      return None
  
  def get_headers() -> dict:
    ua = UserAgent()
    headers = {
        "user-agent": ua.random.strip(),
        "referer": HLTB.BASE_URL,
        "accept": "*/*",
        "content-type": "application/json"
    }
    return headers

  def search_game(title: str) -> dict:
    headers = HLTB.get_headers()

    key = HLTB.get_key()
    payload = HLTB.get_payload(title)
    url = HLTB.SEARCH_URL + key
    res = requests.post(url, headers=headers, data=payload)
    if res.status_code == 200 and len(res.json()['data']) != 0:
      return res.json()['data'][0]

    user_id = HLTB.get_id()
    payload = HLTB.get_payload(title, user_id)
    res = requests.post(HLTB.SEARCH_URL, headers=headers, data=payload)
    if res.status_code == 200 and len(res.json()['data']) != 0:
      return res.json()['data'][0]

    return None

    try:
      return res.json()['data'][0]
    except IndexError:
      return None
  
  def package(data: dict) -> dict:
    """Returns a formated dictionary of HLTB Values"""
    return {
      'id': data['game_id'],
      'main': HLTB.format(data['comp_main']),
      'main_extra': HLTB.format(data['comp_plus']),
      'completionist': HLTB.format(data['comp_100']),
      'all_styles': HLTB.format(data['comp_all'])
    }

  def format(num: int) -> str:
    """Format HowLongToBeat hours by round to the nearest half hour and adding the 1/2 symbol"""
    num_hours = num / 3600
    norm_num = round(num_hours * 2) / 2

    if norm_num%1==0: return str(int(norm_num))
    else: return str(math.floor(norm_num)) + "½"