import requests

from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from src.user import user_bp, signup_bp, signin_bp, support_bp
from src.utils.db_user import db_user

@user_bp.route('/', methods=('GET', 'POST'))
def user():
  return render_template('user/userpage.html')

@signup_bp.route('/', methods=('GET', 'POST'))
def signup():
  response = {
    "status": 200,
    "username": {
      "taken": False,
      "invalid": False
    },
    "password": {
      "invalid": False
    },
    "email": {
      "taken": False,
      "invalid": False
    },
  }
  
  if request.method == 'POST':
    print(request.form)
    user = request.form['username']
    email = request.form["email"]
    password = request.form["password"]
    if user == "": 
      response['username']['invalid'] = True
      response['status'] = 400
    if email == "": 
      response['email']['invalid'] = True
      response['status'] = 400
    if password == "":
      response['password']['invalid'] = True
      response['status'] = 400
    
    dob = request.form.get('dob', None)
    currency = request.form.get('currency', 'USD')
    profile_pic_path = request.form.get('profile_pic_path', None)

    allow_alerts = 'allow_alerts' in request.form
    allow_notifications = 'allow_notifications' in request.form

    if db_user.exists_email(email):
      response['email']['taken'] = True
      response['status'] = 400
    if db_user.exists_user(user):
      response['username']['taken'] = True
      response['status'] = 400
    
    if response['status'] == 200:
      db_user.insert_user(user, password, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications)
      return response, 200
    else: return response, 400
  else: return render_template('user/sign_up.html')

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