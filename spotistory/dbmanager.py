import sqlite3


class dbManager:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def init_db(self):
        self.create_table()

    def create_table(self):
        with open('scripts/create_tables.sql', 'r') as myfile:
            data = myfile.read().replace('\n', ' ')
        c = self.conn.cursor()
        c.executescript(data)
        self.conn.commit()

    def insert_values(self, table_name, elems):
        c = self.conn.cursor()
        for elem in elems:
            values = elem.to_tuple()
            c.execute(
                "INSERT INTO {} VALUES (?{})".format(
                    table_name,
                    "".join([',?' for k in range(len(values) - 1)])
                ),
                values
            )
        self.conn.commit()
