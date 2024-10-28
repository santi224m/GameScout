import psycopg2

def exists_database(db_name):
  """Return True if database already exists, False otherwise"""
  conn = psycopg2.connect(database='postgres')
  curr = conn.cursor()
  curr.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (db_name,))
  res = curr.fetchall()
  conn.close()

  if res:
    return True
  return False

def create_database(db_name):
  """Create a database in postgres"""
  conn = psycopg2.connect(database='postgres')
  curr = conn.cursor()
  conn.autocommit = True
  curr.execute(f"CREATE DATABASE {db_name};")
  conn.close()

def create_tables(db_name):
  """Create tables in the database"""
  conn = psycopg2.connect(database=db_name)
  curr = conn.cursor()

  # User Account
  curr.execute("CREATE TABLE IF NOT EXISTS user_account (id SERIAL PRIMARY KEY, username VARCHAR(20) UNIQUE NOT NULL, password_hash TEXT NOT NULL, dob DATE, currency VARCHAR(3) DEFAULT 'usd', profile_pic_path TEXT, email TEXT, allow_alerts BOOLEAN DEFAULT FALSE, allow_notifications BOOLEAN DEFAULT FALSE);")

  # Game
  curr.execute("CREATE TABLE IF NOT EXISTS game (steam_app_id INT PRIMARY KEY, title TEXT NOT NULL);")

  # Wishlist Item
  curr.execute("CREATE TABLE IF NOT EXISTS wishlist_item (user_account_id INT NOT NULL REFERENCES user_account(id), steam_app_id INT NOT NULL REFERENCES game(steam_app_id), added_date DATE DEFAULT now(), PRIMARY KEY (user_account_id, steam_app_id));")

  # Commit and close connection
  conn.commit()
  conn.close()

def create_user(db_name, username):
  """
  Create a user in the database
  TEMP FUNCTION WHILE WE GET SIGNUP WORKING
  """
  conn = psycopg2.connect(database=db_name)
  curr = conn.cursor()

  curr.execute("INSERT INTO user_account (username, password_hash) VALUES (%s, 'temp_hash') ON CONFLICT (username) DO NOTHING;", (username,))

  conn.commit()
  conn.close()

def setup_db():
  DB_NAME = "gamescout"
  TEST_USER = "user1"
  if not exists_database(DB_NAME):
    create_database(DB_NAME)
  create_tables(DB_NAME)
  create_user(DB_NAME, TEST_USER)

if __name__ == "__main__":
  setup_db()