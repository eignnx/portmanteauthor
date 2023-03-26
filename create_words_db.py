import sqlite3
from os.path import exists


DB_PATH = "./words.db"

def maybe_init():
  if not exists(DB_PATH):
    init()

def init():
  
  conn = sqlite3.connect(DB_PATH)
  c = conn.cursor()
  
  c.execute("""
      CREATE TABLE portmanteau_and_markov
      (word text)
  """)
  
  conn.commit()
  conn.close()

if __name__ == "__main__":
  maybe_init()
