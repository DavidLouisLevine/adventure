class Location:
    def __init__(self, abbreviation, name, moves, response=None):
        self.name = name
        self.moves = list(moves)
        self.abbreviation = abbreviation
        self.responses = response

    def __str__(self):
        return self.abbreviation

class Locations:
    def __init__(self, locations):
        self.items = locations
        for i in range(len(self.items)):
            self.items[i].index = i + 1

    def len(self):
        return len(self.items)

    def __getitem__(self, item):
        if type(item) is str:
            for i in range(len(self.items)):
                if self.items[i].name == item or self.items[i].abbreviation[:3] == item[:3]:
                    return self.items[i]
            return None
        else:
            return self.items[item - 1]