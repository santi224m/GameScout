import requests

from flask import render_template, request, abort
from src.search import bp

@bp.route('/', methods=('GET', 'POST'))
def search_results():
    search_term = request.args['title']
    if search_term == "": abort(400)
    res = requests.get(f'https://www.cheapshark.com/api/1.0/games?title={search_term}')
    res_json = res.json()
    return render_template('search/search_results.html', search_term=search_term, res_json=res_json)
