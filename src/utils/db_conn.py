"""Context manager used to connect to the PostgreSQL database"""
import psycopg2

from flask import current_app

class db_conn:
  def __enter__(self):
    self.conn = psycopg2.connect(database=current_app.config['DB_NAME'])
    self.curr = self.conn.cursor()
    return self.curr

  def __exit__(self, exc_type, exc_value, exc_tb):
    self.conn.commit()
    self.conn.close()

