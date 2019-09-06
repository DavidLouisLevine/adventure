from adventure.items import Items

class Location:
    def __init__(self, abbreviation, name, moves, response=None):
        self.name = name
        self.moves = list(moves)
        self.abbreviation = abbreviation
        self.responses = response

    def __str__(self):
        return self.abbreviation

class Locations(Items):
    def __init__(self, objects):
        Items.__init__(self, objects)

    def Do(self, target, game):
        raise NotImplementedError()
