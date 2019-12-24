class Artist:

    def __init__(self, artist_id, uri, title):
        self.id = artist_id
        self.uri = uri
        self.title = title

    def __str__(self):
        return '{} (id={})'.format(self.title, self.id)

    def to_tuple(self):
        return (self.id, self.uri, self.title)
