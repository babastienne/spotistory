from datetime import datetime


class track:

    def __init__(self, id, uri, played_at):
        self.id = id
        self.uri = uri
        self.played_at = played_at
        self.to_add = True
        self.week_id = datetime.fromtimestamp(played_at).isocalendar()[1]

    def __str__(self):
        return self.id + " " + self.uri + " " + str(self.played_at) + " " + str(self.week_id)

    def to_tuple(self):
        return (self.id, self.uri, self.played_at, self.to_add, self.week_id)
