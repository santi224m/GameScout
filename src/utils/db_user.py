from werkzeug.security import generate_password_hash, check_password_hash

from src.utils.db_conn import db_conn

class db_user:
  def exists_user(username):
    """Returns True if username exists in the database, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM user_account WHERE username = %s;", (username,))
      res = curr.fetchall()
      if res:
        return True
      return False
    
  def exists_email(email):
    """Returns True if email exists in the database, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM user_account WHERE email = %s;", (email,))
      res = curr.fetchall()
      if res:
        return True
      return False
    
  def correct_login(email, password):
    with db_conn() as curr:
      curr.execute("SELECT password_hash FROM user_account WHERE email = %s", (email,))
      res = curr.fetchall()
      if not res: return False
      if not check_password_hash(res[0][0], password): return False
      else: return True

  def insert_user(username, password, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications):
    """Insert a new user to the database"""
    with db_conn() as curr:
      password_hash = generate_password_hash(password)
      curr.execute("INSERT INTO user_account (username, password_hash, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                   (username, password_hash, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications))

  def update_user(original_username, new_username, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications):
    """Update a user in the database"""
    raise NotImplementedError

  def get_user_full(email):
    """
    Return all user details from the database.
    username, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications
    """
    with db_conn() as curr:
      curr.execute("SELECT username, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications FROM user_account WHERE email = %s;", (email,))
      res = curr.fetchone()
      user = {
        'username': res[0],
        'dob': res[1],
        'currency': res[2],
        'profile_pic_path': res[3],
        'email': res[4],
        'allow_alerts': res[5],
        'allow_notifications': res[6]
      }
      return user