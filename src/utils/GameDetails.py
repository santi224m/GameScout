"""The GameDetails class collects and stores game info using various APIs"""
import requests

class GameDetails :
  def __init__(self, steam_app_id):
    if isinstance(steam_app_id, str) and not steam_app_id.isdigit():
      raise ValueError("Steam App ID must be a digit")
    self.steam_app_id = str(steam_app_id)
    self.title = None
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
    self.review_count = None
    self.release_date = None
    self.update_with_steam_api()

  def update_with_steam_api(self):
    """Update game details using Steam API"""
    # Make API call
    usd = 1
    url_params = {'appids': self.steam_app_id, 'currency': usd}
    res = requests.get('https://store.steampowered.com/api/appdetails', params=url_params)
    app_details = res.json()[self.steam_app_id]['data']

    # Update game details
    self.title = app_details['name']
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
    self.review_count = app_details['recommendations']['total']
    self.release_date = app_details['release_date']['date']