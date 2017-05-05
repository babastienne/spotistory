import sqlite3

class db_manager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def init_db(self):
        self.create_table("history")
        self.create_table("playlist")

    def create_table(self, name):
        with open('scripts/create_' + name + '.sql', 'r') as myfile:
            data = myfile.read().replace('\n', ' ')
        c = self.conn.cursor()
        c.execute(data)
        self.conn.commit()

    def add_tracks(self,  tracks):
        c = self.conn.cursor()
        for track in tracks:
            c.execute("INSERT INTO history VALUES(?,?,?,?,?)", track.to_tuple())
        self.conn.commit()

    def get_non_added_tracks(self):
        return self.conn.execute("SELECT * FROM history WHERE to_add=1 ORDER BY played_at ASC").fetchall()

    def set_added(self):
        c = self.conn.cursor()
        c.execute("UPDATE history set to_add=0")
        self.conn.commit()

