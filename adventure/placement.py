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
        Placement.__init__(self)

    def __str__(self):
        return self.location.Name()

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