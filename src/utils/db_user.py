from werkzeug.security import generate_password_hash, check_password_hash

from src.utils.db_conn import db_conn

import random

class db_user:
  def exists_user(username):
    """Returns True if username exists in the database, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM user_account WHERE username = %s;",
                   (username,))
      res = curr.fetchall()
      if res:
        return True
      return False
    
  def exists_email(email):
    """Returns True if email exists in the database, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM user_account WHERE email = %s;", (email.lower(),))
      res = curr.fetchall()
      if res:
        return True
      return False
    
  def correct_login(email, password):
    """Return True if the password matches the email, False otherwise"""
    with db_conn() as curr:
      curr.execute("SELECT password_hash FROM user_account WHERE email = %s", (email,))
      res = curr.fetchall()
      if not res: return False
      if not check_password_hash(res[0][0], password): return False
      else: return True

  def insert_user(username, password, country, email, google=False):
    """Insert a new user to the database"""
    with db_conn() as curr:
      if google: 
        password_hash = None
        if db_user.exists_user(username): username += str(random.randrange(0, 9999))
      else: password_hash = generate_password_hash(password)
      curr.execute(
        """
        INSERT INTO user_account (
          username,
          password_hash,
          country,
          email,
          google)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (username, password_hash, country, email.lower(), google))

  def update_user_email(uuid, email):
    """Update a user's email"""
    with db_conn() as curr:
      #check if new email is not in the database
      if not db_conn.exists_email(email):
        curr.execute("UPDATE user_account SET email = %s WHERE uuid = %s;",
                     (email, uuid))
        return True
      return False
  
  def update_user_password(uuid, password):
    """Updates a users password"""
    password_hash = generate_password_hash(password)
    with db_conn() as curr:
      #check if new email is not in the database
      curr.execute("UPDATE user_account SET password_hash = %s WHERE uuid = %s;",
                   (password_hash, uuid))
      return True

  def update_country(uuid, country):
    """Update a user's country"""
    with db_conn() as curr:
      curr.execute("UPDATE user_account SET country = %s WHERE uuid = %s; ",
                   (country, uuid))
      return True
  
  def get_email_by_uuid(uuid):
    """Get email using uuid"""
    with db_conn() as curr:
      curr.execute("SELECT email FROM user_account WHERE uuid = %s; ", (uuid,))
      res = curr.fetchone()
      return res[0]

  def verify_user(uuid):
    """Verify a user's account"""
    with db_conn() as curr:
      curr.execute("SELECT verified FROM user_account WHERE uuid = %s;",
                   (uuid,))
      res = curr.fetchone()
      if res[0] is True: return False

      curr.execute("UPDATE user_account SET verified = true WHERE uuid = %s;",
                   (uuid,))
      return True

  def get_uuid_by_email(email):
    with db_conn() as curr:
      curr.execute("SELECT uuid FROM user_account WHERE email = %s;", (email.lower(),))
      res = curr.fetchall()
      return res[0][0]

  def get_password_modified(email):
    with db_conn() as curr:
      curr.execute("SELECT TO_CHAR(password_last_modified, 'MM/DD/YYYY') FROM user_account WHERE email = %s;", (email,))
      res = curr.fetchone()
      return res[0]

  def google_login(email):
    with db_conn() as curr:
      curr.execute("SELECT google FROM user_account WHERE email = %s;", (email.lower(),))
      res = curr.fetchone()
      return res[0]

  def get_user_full(email):
    """
    Return user info for session
    """
    with db_conn() as curr:
      curr.execute(
        """
        SELECT  uuid,
                username,
                country,
                email,
                verified,
                TO_CHAR(password_last_modified, 'MM/DD/YYYY'),
                google
        FROM user_account
        WHERE email = %s;
        """, (email.lower(),))

      res = curr.fetchone()
      user = {
        'uuid': res[0],
        'username': res[1],
        'country': res[2],
        'email': res[3],
        'verified': res[4],
        'password_last_modified': res[5],
        'google': res[6]
      }
      return user

  def exists_user_email(username, email):
    """
    Check if username and email exist in database.
    Return dictionary: {"username": bool, "email": bool}
    """
    with db_conn() as curr:
      curr.execute("SELECT 1 FROM user_account WHERE username = %s;",
                   (username,))
      exists_username = True if curr.fetchone() else False

      curr.execute("SELECT 1 FROM user_account WHERE email = %s;",
                   (email.lower(),))
      exists_email = True if curr.fetchone() else False

      data = {
        "username": exists_username,
        "email": exists_email
      }
      return data