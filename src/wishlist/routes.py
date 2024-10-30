from flask import render_template, redirect, url_for, session
from src.wishlist import bp

from src.utils.WishlistDetails import WishlistDetails

@bp.route('/')
def wishlist():
    if 'user' not in session:
        return redirect(url_for('signin.signin'))
    username = session['user']['username']
    wishlist = WishlistDetails(username)
    return render_template('wishlist/wishlist.html', wishlist=wishlist)
