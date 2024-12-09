from flask import render_template, redirect, url_for, session
from src.watchlist import bp

from src.utils.WatchlistDetails import WatchlistDetails
from src.utils.db_utils import db_utils

@bp.route('/')
def watchlist():
    if 'user' not in session:
        session["redirect"] = "watchlist.watchlist"
        return redirect(url_for('signin.signin'))
    username = session['user']['username']
    watchlist = WatchlistDetails(username)
    return render_template('lists/watchlist.html', watchlist=watchlist)
