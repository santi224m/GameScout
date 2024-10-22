import requests

from flask import Blueprint, render_template, request, abort
from src.user import user_bp, signup_bp, signin_bp, support_bp
from src.utils.db_user import db_user

@user_bp.route('/', methods=('GET', 'POST'))
def user():
    return render_template('user/userpage.html')

@signup_bp.route('/', methods=('GET', 'POST'))
def signup():
    username_exists = False
    
    if request.method == 'POST':
        print(request.form)
        user = request.form['username']
        password_input = request.form["password"]
        dob = request.form.get('dob', None)
        currency = request.form.get('currency', 'USD')
        profile_pic_path = request.form.get('profile_pic_path', None)
        email = request.form["email"]
        allow_alerts = request.form.get('allow_alerts', False)
        allow_notifications = request.form.get('allow_notifications', False)
        if db_user.exists_user(user):
            username_exists = True

        db_user.insert_user(user, password_input, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications)
    return render_template('user/sign_up.html', username_exists=username_exists)

@signin_bp.route('/', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        # print(request.form)
        # user = request.form['email']
        # res = db_user.exists_user(user)
        # print(res)
        email = request.form['email']
        res = db_user.exists_email(email)
        print(res)
    return render_template('user/sign_in.html')

@support_bp.route('/', methods=('GET', 'POST'))
def support():
    return render_template('user/support.html')