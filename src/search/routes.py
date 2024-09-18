from flask import render_template, request
from src.search import bp

@bp.route('/', methods=('GET', 'POST'))
def search_results():
    search_term = request.args['title']
    return render_template('search/search_results.html', search_term=search_term)
