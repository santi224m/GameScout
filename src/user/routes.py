import requests

from flask import render_template, request, abort
from src.user import bp



@bp.route('/', methods=('GET', 'POST'))


def user():
    # return render_template
    return render_template('user/userpage.html')


@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    return '<h3> Sign up page </h3>'