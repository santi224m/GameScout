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
      curr.execute("SELECT 6 FROM user_account WHERE username = %s;", (email,))
      res = curr.fetchall()
      if res:
        return True
      return False

  def insert_user(username, password, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications):
    """Insert a new user to the database"""
    with db_conn() as curr:
      password_hash = generate_password_hash(password)
      curr.execute("INSERT INTO user_account (username, password_hash, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
                   (username, password_hash, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications))

  def update_user(original_username, new_username, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications):
    """Update a user in the database"""
    raise NotImplementedError

  def get_user_full(username):
    """
    Return all user details from the database.
    username, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications
    """
    with db_conn() as curr:
      curr.execute("SELECT username, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications FROM user_account WHERE username = %s;", (username,))
      res = curr.fetchall()
      return res