from flask import render_template, redirect, url_for
from src.wishlist import bp

from src.utils.db_utils import db_utils

@bp.route('/')
def wishlist():
    temp_username = "user1"
    users_wishlist = db_utils.get_user_wishlist_items(temp_username)
    return render_template('wishlist/wishlist.html', users_wishlist=users_wishlist)
