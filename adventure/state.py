from adventure.inventory import Inventory

class State:
    def __init__(self):
        self.Init()

    def __getitem__(self, key):
        return self.items[key]

    def __setitem__(self, key, value):
        self.items[key] = value

    def Init(self):
        self.location = None
        self.inventory = Inventory(5, self)
        self.items = dict()
        self.isDead = False
