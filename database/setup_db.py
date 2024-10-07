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
  curr.execute("CREATE TABLE IF NOT EXISTS user_account (id SERIAL PRIMARY KEY, user_name VARCHAR(20));")

  # Wishlist Item
  curr.execute("CREATE TABLE IF NOT EXISTS wishlist_item (user_account_id INT NOT NULL REFERENCES user_account(id), steam_app_id INT NOT NULL);")

  # Commit and close connection
  conn.commit()
  conn.close()

if __name__ == "__main__":
  DB_NAME = "gamescout"
  if not exists_database(DB_NAME):
    create_database(DB_NAME)
  create_tables(DB_NAME)