from flask import Blueprint

bp = Blueprint('user', __name__, static_folder="static", static_url_path='../static/')

from src.user import routes