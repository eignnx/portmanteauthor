import sqlite3
from db_set import DbSet

TEST_DB = "test.db"

conn = sqlite3.connect(TEST_DB)

c = conn.cursor()
c.executemany(
    "INSERT INTO portmanteau_and_markov VALUES (?)",
    [("rabbit",), ("cat",), ("dog",)]
)

s = DbSet(TEST_DB, table="portmanteau_and_markov", col="word")

print("RABBIT IN DB:", "rabbit" in s)
print("QWERTY IN DB:", "qwerty" in s)

