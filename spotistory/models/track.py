class Track:

    def __init__(self, track_id, uri, duration, artist_id, title):
        self.id = track_id
        self.uri = uri
        self.duration = duration
        self.artist_id = artist_id
        self.title = title

    def __str__(self):
        return '{} (id={}) by {}'.format(self.title, self.id, self.artist_id)

    def to_tuple(self):
        return (self.id, self.uri, self.duration, self.artist_id, self.title)
