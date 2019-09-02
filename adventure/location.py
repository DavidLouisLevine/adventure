class Location:
    def __init__(self, abbreviation, name, moves):
        self.name = name
        self.moves = list(moves)
        self.abbreviation = abbreviation

    def __str__(self):
        return self.abbreviation

class Placement:
    def InInventory(self):
        return self.inventory

    def Exists(self):
        return self.exists

class LocationPlacement(Placement):
    def __init__(self, location):
        self.location = location
        self.inventory = False
        self.exists = True

    def __str__(self):
        return self.location.name

class InventoryPlacement(Placement):
    def __init__(self):
        self.location = None
        self.inventory = True
        self.exists = True

    def __str__(self):
        return 'Inventory'

class NoPlacement(Placement):
    def __init__(self):
        self.location = None
        self.inventory = False
        self.exists = None

    def __str__(self):
        return "Doesn't exist"

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