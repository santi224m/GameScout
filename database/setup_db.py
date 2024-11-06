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
  curr.execute("CREATE TABLE IF NOT EXISTS user_account (uuid uuid DEFAULT gen_random_uuid() PRIMARY KEY, username VARCHAR(20) UNIQUE NOT NULL, password_hash TEXT NOT NULL, dob DATE, country VARCHAR(2) DEFAULT 'us', email TEXT, verified BOOLEAN DEFAULT FALSE);")

  # Game
  curr.execute("CREATE TABLE IF NOT EXISTS game (steam_app_id INT PRIMARY KEY, title TEXT NOT NULL);")

  # Wishlist Item
  curr.execute("CREATE TABLE IF NOT EXISTS wishlist_item (user_uuid uuid NOT NULL REFERENCES user_account(uuid), steam_app_id INT NOT NULL REFERENCES game(steam_app_id), added_date DATE DEFAULT now(), rank INT, PRIMARY KEY (user_uuid, steam_app_id));")

  # Trigger function to update rank
  curr.execute("CREATE OR REPLACE FUNCTION set_new_wishlist_rank() RETURNS TRIGGER AS $$ BEGIN SELECT COALESCE(COUNT(*), 0) + 1 FROM wishlist_item WHERE user_uuid = NEW.user_uuid INTO NEW.rank; RETURN NEW; END; $$ LANGUAGE plpgsql;")
  curr.execute("DROP TRIGGER IF EXISTS wishlist_rank_trigger ON wishlist_item;")
  curr.execute("CREATE TRIGGER wishlist_rank_trigger BEFORE INSERT ON wishlist_item FOR EACH ROW EXECUTE FUNCTION set_new_wishlist_rank();")

  # Commit and close connection
  conn.commit()
  conn.close()

def setup_db():
  DB_NAME = "gamescout"
  if not exists_database(DB_NAME):
    create_database(DB_NAME)
  create_tables(DB_NAME)

if __name__ == "__main__":
  setup_db()