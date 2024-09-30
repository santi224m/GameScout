from flask import Blueprint

bp = Blueprint('game', __name__, static_folder="static", static_url_path='../static/')

from src.game import routes