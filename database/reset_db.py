import csv

import psycopg2

from db_conn import db_conn
from setup_db import setup_db

ITAD_IDS_CSV_FNAME = "itad_ids.csv"

def drop_database(db_name):
  """Drop the gamescout database"""
  conn = psycopg2.connect(database='postgres')
  curr = conn.cursor()
  conn.autocommit = True
  curr.execute(f"DROP DATABASE {db_name};")
  conn.commit()
  conn.close()

def store_itad_ids():
  with db_conn() as curr:
    curr.execute("SELECT * FROM itad_game_id;")
    res = curr.fetchall()

  with open(ITAD_IDS_CSV_FNAME, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(res)

def load_itad_ids():
  with open(ITAD_IDS_CSV_FNAME, 'r') as f:
    itad_ids = [tuple(row) for row in csv.reader(f)]

  with db_conn() as curr:
    for steamappid, itad_id in itad_ids:
      curr.execute(
        """
        INSERT INTO itad_game_id (steam_app_id, itad_id)
        VALUES (%s, %s)
        ON CONFLICT (steam_app_id) DO UPDATE
          SET itad_id = %s;
        """, (steamappid, itad_id, itad_id))

if __name__ == "__main__":
  DB_NAME = "gamescout"
  store_itad_ids()
  drop_database(DB_NAME)
  setup_db()
  load_itad_ids()