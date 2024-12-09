from flask import Blueprint

terms_bp = Blueprint('terms', __name__, static_folder="static", static_url_path='../static/')
privacy_bp = Blueprint('privacy', __name__, static_folder="static", static_url_path='../static/')

from src.policies import routes