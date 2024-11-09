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

  def insert_user(username, password, dob, country, email):
    """Insert a new user to the database"""
    with db_conn() as curr:
      password_hash = generate_password_hash(password)
      curr.execute("INSERT INTO user_account (username, password_hash, dob, country, email) VALUES (%s, %s, %s, %s, %s);",
                   (username, password_hash, dob, country, email,))
  
  def update_user_email(uuid, email):
    """Update user email to the database"""
    with db_conn() as curr:
      #check if new email is not in the database
      if not db_conn.exists_email(email):
        curr.execute("UPDATE user_account SET email = %s WHERE uuid = %s; ",(email, uuid))
        return True
      else:
        return False

  def update_country(uuid, country):
    """Update user country to the data base """
    with db_conn() as curr:
      curr.execute("UPDATE user_account SET country = %s WHERE uuid = %s; ",(country, uuid))
      return True
  
  def get_email_by_uuid(uuid):
    """Get email using uuid"""
    with db_conn() as curr:
      curr.execute("SELECT email FROM user_account WHERE uuid = %s; ", (uuid,))
      res = curr.fetchone()
      return res[0]

  def verify_user(id):
    with db_conn() as curr:
      curr.execute("SELECT verified FROM user_account WHERE uuid = %s;", (id,))
      res = curr.fetchall()
      if res[0][0]: return False
      else: 
        curr.execute("UPDATE user_account SET verified = true WHERE uuid = %s", (id,))
        return True

  def get_uuid_by_email(email):
    with db_conn() as curr:
      curr.execute("SELECT uuid FROM user_account WHERE email = %s;", (email,))
      res = curr.fetchall()
      return res[0][0]

  def get_user_full(email):
    """
    Return all user details from the database.
    uuid, username, dob, currency, email, verified
    """
    with db_conn() as curr:
      curr.execute("SELECT uuid, username, dob, country, email, verified, TO_CHAR(password_last_modified, 'MM/DD/YYYY') FROM user_account WHERE email = %s;", (email,))
      res = curr.fetchone()
      user = {
        'uuid': res[0],
        'username': res[1],
        'dob': res[2],
        'country': res[3],
        'email': res[4],
        'verified': res[5],
        'password_last_modified': res[6]
      }
      return user
    
  def exists_user_email(username, email):
    with db_conn() as curr:
      curr.execute("(SELECT 1 FROM user_account WHERE username = %s) UNION (SELECT 2 FROM user_account WHERE email = %s);", (username, email,))
      res = curr.fetchall()

      data = {
        "username": False,
        "email": False
      }
      if not res: return data
      if 1 in res[0]: data['username'] = True
      if 2 in res[1]: data['email'] = True
      return data