from adventure.location import InventoryPlacement, LocationPlacement

class Inventory:
    def __init__(self, capacity, state, world):
        self.capacity = capacity
        self.size = 0
        self.state = state
        self.world = world

    def Get(self):
        items = ()
        for object in self.world.objects:
            if object.placement.InInventory():
                items += (object, )
        return items

    def GetStrings(self):
        items = ()
        for object in self.world.objects:
            if object.placement.InInventory():
                items += (str(object), )
        return items

    def Has(self, object):
        return object.placement.InInventory()

    def Add(self, object):
        if self.size != self.capacity:
            object.placement = InventoryPlacement()
            self.size += 1
            assert(self.size <= self.capacity)
            return True
        else:
            return False

    def Remove(self, object, location):
        if self.Has(object):
            object.placement = LocationPlacement(location)
            self.size -= 1
            assert(self.size >= 0)
            return True
        else:
            return False

    def __str__(self):
        return '(' + ', '.join(self.GetStrings()) + ')'