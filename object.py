import copy
from direction import Direction

class Objects:
    def __init__(self, items):
        self.items = ()
        for i in range(len(items)):
            assert type(items[i]) is Object
            newitem = copy.copy(items[i])
            newitem.n = i
            self.items += (newitem,)

    def len(self):
        return len(self.items)

    def __getitem__(self, item):
        if type(item) is str:
            return self.Find(item)
        else:
            return self.items[item - 1]

    def Find(self, item, location=None):
        for i in range(len(self.items)):
            if self.items[i].name == item or self.items[i].abbreviation == item[:3]:
                if location is None or self.items[i].placement.location == location:
                    return self.items[i]
        return None

    def Add(self, items):
        self.items += items

class Object:
    def __init__(self, name, abbreviation, placement, response=None, moveable=False, lookable=True):
        self.name = name
        self.abbreviation = abbreviation
        self.placement = placement
        self.response = response
        self.moveable = moveable
        self.lookable = lookable

class Action:
    def __init__(self, verb, target):
        self.verb = verb
        self.target = target

class Target:
    def __init__(self, value, world, state):
        if type(value) is str:
            if Direction.IsValid(value):
                self.value = Direction(value)
            elif state.location is None:
                self.value = world.objects[value]
            else:
                object = world.objects.Find(value)
                if object is not None and state.inventory.Has(object):
                    self.value = object
                else:
                    self.value = world.objects.Find(value, state.location)
        elif type(value) is Direction or type(value) is Object:
            self.value = value
        else:
            assert("Unknown type: {0}".format(type(value)))

    def IsDirection(self):
        return type(self.value) is Direction

    def IsObject(self):
        return type(self.value) is Object