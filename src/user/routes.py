import re
import threading

from flask import render_template, request, session, redirect, url_for, current_app
from src.user import account_bp, signup_bp, signin_bp, support_bp
from src.utils.db_user import db_user
from src.utils.ImageHandler import ImageHandler
from src.utils.MailSender import MailSender

from src.utils.JWTGenerator import JWTGen

tasks = set()

@account_bp.route('/', methods=('GET', 'POST'))
def user():
  if 'user' in session:
    if request.method == 'GET': return render_template('user/account.html')
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
    
    dob = request.form.get('dob', None)
    country = request.form.get('country', 'us')

    exists = db_user.exists_user_email(username, email)
    if exists['username']: response['username']['taken'] = True
    if exists['email']: response['email']['taken'] = True

    if True not in response['username'].values() and True not in response['email'].values() and True not in response['password'].values():
      session['signin'] = True

      thread_db = threading.Thread(db_user.insert_user(username, password, dob, country, email))
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

@account_bp.route('/password', methods=('GET', 'POST'))
def reset_password():
  if request.method == "GET":
    if 'user' in session:
      print(JWTGen.encode_jwt(session['user']['email'], session['user']['uuid'], 'password'))
    return redirect(url_for('account.user'))
  if request.method == "POST":
    email = request.form["email"]
    if email == "" or not re.search(".+[@].+(?<![.])$", email) or not db_user.exists_email(email): 
      return "invallid email"
    uuid = db_user.get_uuid_by_email(email)
    print(JWTGen.encode_jwt(email, uuid, 'password'))

    return redirect(url_for('account.user'))