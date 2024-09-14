import requests

from flask import render_template
from src.main import bp

@bp.route('/', defaults={'steam_app_id': 620})
@bp.route('/<steam_app_id>')
def index(steam_app_id):
    url_params = {'appids': steam_app_id}
    res = requests.get('https://store.steampowered.com/api/appdetails', params=url_params)
    app_details = res.json()
    return render_template('index.html', steam_app_id=steam_app_id, app_details=app_details)
