import requests

from flask import render_template, request, abort
from src.search import bp

from src.utils.SearchDetails import SearchDetails

@bp.route('/', methods=('GET', 'POST'))
def search_results():
    # Get Args
    search_term = request.args['t']
    engine = request.args['e']

    # Abort if Title is blank
    if search_term == "": abort(400)

    # Temp Hack for dual search engine
    if engine == "cs":
        res = requests.get(f'https://www.cheapshark.com/api/1.0/games?title={search_term}')
        res_json = res.json()
        return render_template('search/search_results.html', search_term=search_term, engine=engine, res_json=res_json)
    elif engine == "s":
        data = SearchDetails(search_term)
        return render_template('search/search_results.html', search_term=search_term, engine=engine, search_data=data)
    else: abort(400)
