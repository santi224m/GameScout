from flask import Blueprint

user_bp = Blueprint('user', __name__, static_folder="static", static_url_path='../static/')
signup_bp = Blueprint('signup', __name__, static_folder="static", static_url_path='../static/')
signin_bp = Blueprint('signin', __name__, static_folder="static", static_url_path='../static/')

from src.user import routes