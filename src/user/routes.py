import re
import threading
import base64
import os
from dotenv import load_dotenv

from google.oauth2 import id_token
from google.auth.transport import requests

from flask import render_template, request, session, redirect, url_for, current_app
from src.user import account_bp, signup_bp, signin_bp, support_bp
from src.utils.db_user import db_user
from src.utils.ImageHandler import ImageHandler
from src.utils.MailSender import MailSender

from src.utils.JWTGenerator import JWTGen

tasks = set()

load_dotenv()

@account_bp.route('/', methods=('GET', 'POST'))
def user():
  if 'user' in session:
    if request.method == 'GET': 
      if 'v' in session:
        del session['v']
        return render_template('user/account.html', v=True)
      return render_template('user/account.html')
    elif request.method == 'POST':
      print(request.form)
      print(request.files)
      uuid = session['user']['uuid']
      if "pfp" in request.files and request.files['pfp'].filename != "":
        ImageHandler.upload_image(uuid, request.files['pfp'])
        session['user']['pfp'] = ImageHandler.get_image_url(uuid)
      if "country_code" in request.form: 
        session['user']['country'] = request.form['country_code']
        db_user.update_country(session['user']['uuid'], request.form['country_code'])
      return redirect(url_for('account.user'))
  else: 
    session["redirect"] = "account.user"
    return redirect(url_for("signin.signin"))

@signup_bp.route('/', methods=('GET', 'POST'))
def signup():  
  if "signin" in session:
    del session['signin']
    return redirect(url_for("signin.signin"))
  if request.method == 'POST':
    if 'credential' in request.form:
      try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(request.form['credential'], requests.Request(), os.getenv("GOOGLE_OAUTH_KEY"))

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If the request specified a Google Workspace domain
        # if idinfo['hd'] != DOMAIN_NAME:
        #     raise ValueError('Wrong domain name.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        email = idinfo['email']
        name = idinfo['name']
        print(name)
        print(email)
        
        if db_user.exists_email(email) and db_user.google_login(email):
          user = db_user.get_user_full(email)
          session['user'] = user
          session['user']['pfp'] = ImageHandler.get_image_url(user['uuid'])
          return redirect(url_for("main.index"))
        elif db_user.exists_email(email) and db_user.google_login(email) is False: 
          session['g'] = False
          return redirect(url_for("signin.signin"))
        elif db_user.exists_email(email) is False:
          db_user.insert_user(name, None, "us", email, True)
          uuid = db_user.get_uuid_by_email(email)
          db_user.verify_user(uuid)
          ImageHandler.create_blank_pfp(uuid)
          user = db_user.get_user_full(email)
          session['user'] = user
          session['user']['pfp'] = ImageHandler.get_image_url(user['uuid'])
          return redirect(url_for("main.index"))
        else: return redirect(url_for("signup.signup")) # Ignore and redirect back to signup
      except ValueError:
        return redirect(url_for("signup.signup"))
    response = {
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

    username = request.form['username']
    email = request.form["email"]
    password = request.form["password"]
    if username == "" or len(username) > 20: 
      response['username']['invalid'] = True
    if email == "" or not re.search(".+[@].+(?<![.])$", email): 
      response['email']['invalid'] = True
    if len(password) < 8:
      response['password']['invalid'] = True
    
    country = request.form.get('country', 'us')

    exists = db_user.exists_user_email(username, email)
    if exists['username']: response['username']['taken'] = True
    if exists['email']: response['email']['taken'] = True

    if True not in response['username'].values() and True not in response['email'].values() and True not in response['password'].values():
      session['signin'] = True

      thread_db = threading.Thread(db_user.insert_user(username, password, country, email))
      thread_db.start()
      thread_db.join()

      uuid = db_user.get_uuid_by_email(email)

      # thread_mail = threading.Thread(MailSender().send_verification_email(uuid, email, username))
      # thread_mail.start()
      # thread_mail.join()
      
      thread_img = threading.Thread(target=ImageHandler.create_blank_pfp(uuid))
      thread_img.start()
      thread_img.join()

      return response, 200
    else: return response, 400
  else: return render_template('user/sign_up.html')

@signin_bp.route('/', methods=('GET', 'POST'))
def signin():
  if request.method == 'POST':
    email = request.form["email"].lower()
    if db_user.google_login(email):
      return render_template('user/sign_in.html', google=True)
    password = request.form["password"]
    if password == "" or email == "": return render_template('user/sign_in.html', error=True)
    if not db_user.correct_login(email, password): return render_template('user/sign_in.html', error=True)
    else:
      user = db_user.get_user_full(email)
      session['user'] = user
      session['user']['pfp'] = ImageHandler.get_image_url(user['uuid'])
      if "redirect" in session and "verify" in session['redirect'] and "jwt" in session:
        url = session["redirect"]
        jwt = session["jwt"]
        del session["redirect"]
        del session["jwt"]
        return redirect(f"http://127.0.0.1:5000/verify/{jwt}")
      elif "redirect" in session: 
        url = session["redirect"]
        del session["redirect"]
        if ("http://localhost:5000" in url or "http://127.0.0.1:5000" in url) and ("signup" in url or "signin" in url or "signout" in url): return redirect(url_for('main.index'))
        elif "http://localhost:5000" in url or "http://127.0.0.1:5000" in url and "signup" not in url: return redirect(url)
        else: return redirect(url_for(url))
      else: return redirect(url_for('main.index'))
  else: 
    referrer = None
    if request.referrer and ("http://localhost:5000" in request.referrer or "http://127.0.0.1:5000" in request.referrer): referrer = request.referrer
    if referrer: session['redirect'] = referrer
    if 'g' in session: 
      temp = session['g']
      del session['g']
      return render_template('user/sign_in.html', google=temp)
    return render_template('user/sign_in.html')

@account_bp.route('/signout', methods=('GET', 'POST'))
def signout():
  if 'user' in session:
    del session['user']
    if request.referrer and ("http://localhost:5000" in request.referrer or "http://127.0.0.1:5000" in request.referrer) and not ("wishlist" in request.referrer or "account" in request.referrer): return redirect(request.referrer)
  return redirect(url_for('main.index'))

@account_bp.route('/resend_email', methods=('GET', 'POST'))
def resend_email():
  if 'user' in session: 
    MailSender().send_verification_email(session['user']['uuid'], session['user']['email'], session['user']['username'])
    return redirect(url_for('account.user'))
  else: return redirect(url_for('main.index'))

@account_bp.route('/recovery/<jwt>', methods=('GET', 'POST'))
def recover_account(jwt):
  if not jwt: return redirect(url_for('main.index')) 
  claims = JWTGen.decode_jwt(jwt)
  if claims is False: return redirect(url_for('main.index')) 
  modify_date = db_user.get_password_modified(claims['email'])
  claims_date = base64.b64decode(claims['nonce'].encode("ascii")).decode("ascii")
  if modify_date != claims_date: return redirect(url_for('main.index'))

  if request.method == "GET":
    return render_template('user/passwords.html')
  if request.method == "POST":
    password = request.form["password"]
    if len(password) < 8:
      return render_template('user/passwords.html')
    
    db_user.update_user_password(claims['uuid'], password)

    return redirect(url_for("signin.signin"))


@account_bp.route('/password', methods=('GET', 'POST'))
def reset_password():
  if request.method == "GET":
    if 'user' in session:
      MailSender().send_reset_email(session['user']['uuid'], session['user']['email'])
      session['v'] = True
      return redirect(url_for('account.user'))
    else: return render_template('user/recovery.html')
  if request.method == "POST":
    email = request.form["email"]
    if email == "" or not re.search(".+[@].+(?<![.])$", email) or not db_user.exists_email(email): 
      return render_template('user/recovery.html', email=False)
    uuid = db_user.get_uuid_by_email(email)
    MailSender().send_reset_email(uuid, email)

    return render_template('user/recovery.html', email=True)