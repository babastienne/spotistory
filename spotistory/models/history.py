class History:

    def __init__(self, track_id, played_at):
        self.id = track_id
        self.played_at = played_at

    def __str__(self):
        return '{} played at {}'.format(self.id, self.played_at)

    def to_tuple(self):
        return (self.id, self.played_at)
