from flask import render_template, redirect, url_for
from src.wishlist import bp

from src.utils.WishlistDetails import WishlistDetails

@bp.route('/')
def wishlist():
    wishlist = WishlistDetails()
    return render_template('wishlist/wishlist.html', wishlist=wishlist)
