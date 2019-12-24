class Genre:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def to_tuple(self):
        return (self.name)
