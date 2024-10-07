from flask import Blueprint

bp = Blueprint('api', __name__, static_folder="static", static_url_path='../static/')

from src.api import routes