import sqlite3

DB_PATH = "./words.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("""
    CREATE TABLE portmanteau_and_markov
    (word text)
""")

conn.commit()
conn.close()
