from adventure.placement import InventoryPlacement, NoPlacement

class Inventory:
    def __init__(self, capacity, state):
        self.capacity = capacity
        self.size = 0
        self.state = state

    def Get(self, world):
        items = ()
        for object in world.objects:
            if object.placement.InInventory():
                items += (object, )
        return items

    def GetStrings(self, world):
        items = ()
        for object in world.objects:
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

    def Remove(self, object):
        if self.Has(object):
            self.size -= 1
            object.placement = NoPlacement()
            assert(self.size >= 0)
            return True
        else:
            return False

    def string(self, world):
        return '(' + ', '.join(self.GetStrings(world)) + ')'