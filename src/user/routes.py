import requests

from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from src.user import user_bp, signup_bp, signin_bp, support_bp
from src.utils.db_user import db_user

@user_bp.route('/', methods=('GET', 'POST'))
def user():
    return render_template('user/userpage.html')

@signup_bp.route('/', methods=('GET', 'POST'))
def signup():
    error = None
  
    if request.method == 'POST':
        print(request.form)
        user = request.form['username']
        password_input = request.form["password"]
        dob = request.form.get('dob', None)
        currency = request.form.get('currency', 'USD')
        profile_pic_path = request.form.get('profile_pic_path', None)
        email = request.form["email"]

        allow_alerts = 'allow_alerts' in request.form
        allow_notifications = 'allow_notifications' in request.form


        if db_user.exists_email(email):
            error = "Email already exists!"

        # Check if the username already exists
        elif db_user.exists_user(user):
            error = "Username already exists!"
        else:
            db_user.insert_user(user, password_input, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications)
            success_message = "User successfully created!"
            return render_template('user/sign_in.html', success=success_message)

    return render_template('user/sign_up.html', error=error)

@signin_bp.route('/', methods=('GET', 'POST'))
def signin():
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
        res = db_user.exists_email(email)
        if not res: #if email is not in the database
            return render_template('user/sign_in.html', error="Email doesn't exist!")
        else:
            pass
    return render_template('user/sign_in.html')

@support_bp.route('/', methods=('GET', 'POST'))
def support():
    return render_template('user/support.html')