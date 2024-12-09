from flask import Blueprint

bp = Blueprint('watchlist', __name__)

from src.watchlist import routes