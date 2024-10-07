from flask import Blueprint

bp = Blueprint('wishlist', __name__)

from src.wishlist import routes