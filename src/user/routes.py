import requests

from flask import Blueprint, render_template, request, abort
from src.user import user_bp, signup_bp, signin_bp, support_bp
from src.utils.db_user import db_user

@user_bp.route('/', methods=('GET', 'POST'))
def user():
    return render_template('user/userpage.html')

@signup_bp.route('/', methods=('GET', 'POST'))
def signup():
    return render_template('user/sign_up.html')

@signin_bp.route('/', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        print(request.form)
        user = request.form['email']
        res = db_user.exists_user(user)
        print(res)
    return render_template('user/sign_in.html')

@support_bp.route('/', methods=('GET', 'POST'))
def support():
    return render_template('user/support.html')