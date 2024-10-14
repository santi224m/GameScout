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

  def insert_user(username, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications):
    """Insert a new user to the database"""
    raise NotImplementedError

  def update_user(original_username, new_username, dob, currency, profile_pic_path, email, allow_alerts, allow_notifications):
    """Update a user in the database"""
    raise NotImplementedError

  def get_user(username):
    """Return user info"""
    raise NotImplementedError