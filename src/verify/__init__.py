from flask import Blueprint

bp = Blueprint('verify', __name__, static_folder="static", static_url_path='../static/')

from src.verify import routes