import sqlite3

class DbSet:
    """
    >>> s = DbSet("my_data.db", table="my_table", col="word")
    >>> "rabbit" in s
    False
    >>> s.add("rabbit")
    """
    
    def __init__(self, db_file, *, table, col):
        self.db_file = db_file
        self.table = table.split()[0]
        self.col = col.split()[0]

    def __contains__(self, x):
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            query = f"""
                SELECT {self.col}
                FROM {self.table}
                WHERE {self.col} = ?
            """
            c.execute(query, (x,))
            res = c.fetchone()
            return res is not None

    def add(self, x):
        with sqlite3.connect(self.db_file) as conn:
            c = conn.cursor()
            query = f"""
                INSERT INTO {self.table}
                VALUES (?)
            """
            c.execute(query, (x,))
            conn.commit()


