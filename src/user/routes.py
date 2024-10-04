import requests

from flask import Blueprint, render_template, request, abort
from src.user import bp



@bp.route('/', methods=('GET', 'POST'))
def user():
    # return render_template
    return '<h3>hotdog</h3>'
    #return render_template('user/userpage.html')


@bp.route('/signup', methods=('GET', 'POST'))
def signup():
    return render_template('user/sign_up.html')