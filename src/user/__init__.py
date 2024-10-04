from flask import Blueprint

bp = Blueprint('search', __name__, static_folder="static", static_url_path='../static/')

from src.search import routes