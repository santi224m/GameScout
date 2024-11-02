from flask import Blueprint

account_bp = Blueprint('account', __name__, static_folder="static", static_url_path='../static/')
signup_bp = Blueprint('signup', __name__, static_folder="static", static_url_path='../static/')
signin_bp = Blueprint('signin', __name__, static_folder="static", static_url_path='../static/')
support_bp = Blueprint('support', __name__, static_folder="static", static_url_path='../static/')

from src.user import routes