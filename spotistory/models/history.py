class History:

    def __init__(self, track_id, played_at, user_id):
        self.id = track_id
        self.played_at = played_at
        self.user_id = user_id

    def __str__(self):
        return '{} played at {} by {}'.format(self.id, self.played_at, self.user_id)

    def to_tuple(self):
        return (self.id, self.played_at, self.user_id)
