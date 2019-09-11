from adventure.item import Items, Item
import random

class Location:
    def __init__(self, abbreviation, name, moves, response=None):
        Item.__init__(self, name, abbreviation)
        self.moves = list(moves)
        self.responses = response

    def Name(self):
        if type(self.name) is str:
            return self.name

        l = len(self.name)
        if l == 1:
            return self.name
        n = random.choice(range(len(self.name)))
        return self.name[n]

    def __str__(self):
        return self.abbreviation

class Locations(Items):
    def __init__(self, objects):
        Items.__init__(self, objects)

    def Do(self, target, game):
        raise NotImplementedError()
