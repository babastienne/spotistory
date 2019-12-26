class User:

    def __init__(self, id, name, followers, uri):
        self.id = id
        self.name = name
        self.followers = followers
        self.uri = uri

    def __str__(self):
        return '{} ({} followers)'.format(self.name, self.followers)

    def to_tuple(self):
        return (self.name, self.id, self.uri, self.followers)
