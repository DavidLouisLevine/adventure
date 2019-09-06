from adventure.item import Items, Item

class Location:
    def __init__(self, abbreviation, name, moves, response=None):
        Item.__init__(self, name, abbreviation)
        self.moves = list(moves)
        self.responses = response

    def __str__(self):
        return self.abbreviation

class Locations(Items):
    def __init__(self, objects):
        Items.__init__(self, objects)

    def Do(self, target, game):
        raise NotImplementedError()
