from flask import render_template, redirect, url_for
from src.game import bp

from src.utils.GameDetails import GameDetails
from src.utils.db_utils import db_utils

@bp.route('/<steam_app_id>')
def game(steam_app_id):
    # Redirect user to home page if steam_app_id is invalid
    if not steam_app_id.isdigit():
        return redirect(url_for('main.index'))
    game_details = GameDetails(steam_app_id)
    return render_template('game/game_page.html', game=game_details)
