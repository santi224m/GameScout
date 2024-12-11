import cloudinary.exceptions
from dotenv import load_dotenv

load_dotenv()

import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

config = cloudinary.config(
  secure=True
  cloud_name="gamescout"
)

class ImageHandler:
  def create_blank_pfp(name):
    ImageHandler.upload_image(name, "src/static/img/pfp_blank.webp")
  def upload_image(name, file):
    cloudinary.uploader.upload(file, public_id=name, asset_id=name, unique_filename = False, overwrite = True, folder="user")
  def get_image_url(name):
    data = ImageHandler.get_image_info(name)
    return {
      30: "https://res.cloudinary.com/gamescout/image/upload/c_fill,f_auto,g_center,h_30,w_30/v" + str(data['version']) + "/" + data['public_id'],
      100: "https://res.cloudinary.com/gamescout/image/upload/c_fill,f_auto,g_center,h_100,w_100/v" + str(data['version']) + "/" + data['public_id'],
      500: "https://res.cloudinary.com/gamescout/image/upload/c_fill,f_auto,g_center,h_500,w_500/v" + str(data['version']) + "/" + data['public_id'],
      1000: "https://res.cloudinary.com/gamescout/image/upload/c_fill,f_auto,g_center,h_1000,w_1000/v" + str(data['version']) + "/" + data['public_id'],
      "source": "https://res.cloudinary.com/gamescout/image/upload/f_auto/v" + str(data['version']) + "/" + data['public_id']
    }
  def append_version(name):
    data = ImageHandler.get_image_info(name)
    return "#" + str(data['version'])
  def get_image_info(name):
    return cloudinary.api.resource("user/" + name)
  def image_exists(name):
    try: 
      cloudinary.api.resource("user/" + name)
      return True
    except cloudinary.exceptions.NotFound: return False
  def remove_image(name):
    if not ImageHandler.image_exists(name): return False
    cloudinary.uploader.destroy("user/" + name, invalidate=True)
    return True
  def clear_db(confirm = False):
    if confirm: 
      cloudinary.api.delete_all_resources()
      return True
    else: return False