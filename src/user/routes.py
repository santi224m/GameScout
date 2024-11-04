import re
import threading

from flask import render_template, request, session, redirect, url_for, current_app
from src.user import account_bp, signup_bp, signin_bp, support_bp
from src.utils.db_user import db_user
from src.utils.ImageHandler import ImageHandler
from src.utils.MailSender import MailSender

tasks = set()

@account_bp.route('/', methods=('GET', 'POST'))
def user():
  if 'user' in session:
    if request.method == 'GET': return render_template('user/account.html')
    elif request.method == 'POST':
      print(request.files)
      uuid = session['user']['uuid']
      ImageHandler.upload_image(uuid, request.files['pfp'])
      session['user']['pfp'] = ImageHandler.get_image_url(uuid)
      return redirect(url_for('account.user')) 
  else: 
    session["redirect"] = "account.user"
    return redirect(url_for("signin.signin"))

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
    username = request.form['username']
    email = request.form["email"]
    password = request.form["password"]
    if username == "" or len(username) > 20: 
      response['username']['invalid'] = True
      response['status'] = 400
    if email == "" or not re.search(".+[@].+(?<![.])$", email): 
      response['email']['invalid'] = True
      response['status'] = 400
    if len(password) < 8:
      response['password']['invalid'] = True
      response['status'] = 400
    
    dob = request.form.get('dob', None)
    currency = request.form.get('currency', 'USD')

    if db_user.exists_email(email):
      response['email']['taken'] = True
      response['status'] = 400
    if db_user.exists_user(username):
      response['username']['taken'] = True
      response['status'] = 400
    
    if response['status'] == 200:
      db_user.insert_user(username, password, dob, currency, email)
      uuid = db_user.get_uuid_by_email(email)

      # MailSender().send_verification_email(uuid, email, username)
      
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
        if ("http://localhost:5000" in url or "http://127.0.0.1:5000" in url) and "signup" not in url: return redirect(url)
        return redirect(url_for(url))
      else: return redirect(url_for('main.index'))
  else: 
    referrer = None
    if request.referrer and ("http://localhost:5000" in request.referrer or "http://127.0.0.1:5000" in request.referrer): referrer = request.referrer
    if referrer: session['redirect'] = referrer
    return render_template('user/sign_in.html')

@account_bp.route('/signout', methods=('GET', 'POST'))
def signout():
  if 'user' in session:
    del session['user']
    if ("http://localhost:5000" in request.referrer or "http://127.0.0.1:5000" in request.referrer) and not ("wishlist" in request.referrer or "account" in request.referrer): return redirect(request.referrer)
  return redirect(url_for('main.index'))

@support_bp.route('/', methods=('GET', 'POST'))
def support():
  return render_template('user/support.html')