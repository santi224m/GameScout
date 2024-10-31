from pathlib import Path

from flask import render_template, request, session, redirect, url_for, current_app
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
    email = request.form["email"]
    password = request.form["password"]
    if password == "" or email == "": return render_template('user/sign_in.html', error=True)
    if not db_user.correct_login(email, password): return render_template('user/sign_in.html', error=True)
    else:
      user = db_user.get_user_full(email)
      session['user'] = user
      profile_pic = find_profile_pic(user['username'])
      session['user']['profile_pic'] = profile_pic
      return redirect(url_for('main.index'))
  else: return render_template('user/sign_in.html')

@user_bp.route('/signout', methods=('GET', 'POST'))
def signout():
  if 'user' in session:
    del session['user']
  return redirect(url_for('main.index'))

@support_bp.route('/', methods=('GET', 'POST'))
def support():
  return render_template('user/support.html')

def find_profile_pic(username):
  """
  Return the profile pic path for the user.
  Filename should be the username
  and stored in /static/profile_pics/
  """
  image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
  base_path = Path(current_app.config['BASE_DIR'] + "/src/static/profile_pics/")
  for ext in image_extensions:
    fname = base_path / f"{username}{ext}"
    if fname.exists():
      return f"{username}{ext}"
  return None
