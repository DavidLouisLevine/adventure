from location import PlacementLocation, InventoryLocation, Locations
from verb import BuiltInVerbs
from object import Objects, Target
from direction import Direction

class Game:
    def __init__(self, world, state):
        self.world = world
        self.state = state
        self.quitting = False

    def DoAction(self, action):
        try:
            i = action.index(' ')
            verbName = action[:i]
            objectName = action[i + 1:]
        except:
            verbName = action
            objectName = None

        verb = self.world.verbs[verbName]
        if objectName is None:
            target = None
        else:
            direction = Direction.FromName(objectName)
            if not direction is None:
                target = Target(direction, self.world, self.state)
            else:
                target = Target(objectName, self.world, self.state)

        return verb.Do(target, self)

    def Do(self, action, echo=True):
        if echo:
            print("> ", action)
        m = self.DoAction(action)
        if not m is None and not m == "":
            print(m)

    def Run(self, actions):
        i = 0
        prompt = "WHAT DO YOU THINK WE SHOULD DO? "
        while not self.quitting:
            if i < len(actions):
                str = actions[i]
                print(prompt + str)
            else:
                str = input(prompt)
            self.Do(str, echo=False)
            i += 1

    def Look(self):
        return self.world.verbs['LOOK'].Do(None, self)

class World:
    def __init__(self, objects, verbs):
        self.locations = Locations()
        self.verbs = verbs
        self.objects = Objects(objects)
        for object in self.objects:
            if type(object.placement) is int:
                object.placement = PlacementLocation(self.locations[object.placement])

    def AtLocation(self, location):
        l = ()
        for object in self.objects:
            if type(object.placement) is PlacementLocation and object.placement.location == location:
                l += (object, )
        return l

    def print(self):
        s = ""
        for i in range(self.locations.len()):
            print(i + 1, self.locations[i + 1].name, self.locations[i + 1].moves)

        for i in range(self.objects.len()):
            o = self.objects[i]
            print(i, o.name, o.placement)

        for i in range(self.verbs.len()):
            print(i, self.verbs[i].name)

class State:
    def __init__(self, location, world):
        self.location = location
        self.inventory = Inventory(5, self, world)

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

    def Has(self, object):
        return object.placement.InInventory()

    def Add(self, object):
        if self.size != self.capacity:
            object.placement = InventoryLocation()
            self.size += 1
            assert(self.size <= self.capacity)
            return True
        else:
            return False

    def Remove(self, object, location):
        object.placement = PlacementLocation(location)
        self.size -= 1
        assert(self.size >= 0)

class Response:
    def __init__(self, verb, f):
        self.verb = verb
        self.f = f
