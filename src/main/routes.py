from flask import render_template
from src.main import bp

from src.utils.HomeDetails import HomeDetails

@bp.route('/')
def index():
    home_details = HomeDetails()
    return render_template('index.html', home=home_details)
