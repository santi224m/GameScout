import requests

from flask import render_template
from src.main import bp

from src.utils.GameDetails import GameDetails

@bp.route('/', defaults={'steam_app_id': 620})
@bp.route('/<steam_app_id>')
def index(steam_app_id):
    game_details = GameDetails(steam_app_id)
    return render_template('index.html', game_details=game_details)
