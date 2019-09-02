from adventure.location import Locations, LocationPlacement, NoPlacement, Location
from adventure.object import Objects, Object

class World:
    def __init__(self, objects, verbs, locations):
        self.locations = Locations(locations)
        self.verbs = verbs
        self.objects = Objects(objects)
        for object in self.objects:
            if type(object.placement) is int:
                object.placement = LocationPlacement(self.locations[object.placement])

    def AtLocation(self, location):
        l = ()
        for object in self.objects:
            if type(object.placement) is LocationPlacement and object.placement.location == location:
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

    def MoveObject(self, object, location):
        object = self.ResolveObject(object)
        location = self.ResolveLocation(location)
        object.placement = LocationPlacement(location)

    def RemoveObject(self, object):
        object = self.ResolveObject(object)
        object.placement = NoPlacement()

    @staticmethod
    def Resolve(item, t, list):
        if type(item) is t:
            return item
        elif type(item) is str:
            return list[item]
        else:
            assert 'Unknown object type to resolved:', type(item)

    def ResolveObject(self, item):
        return World.Resolve(item, Object, self.objects)

    def ResolveLocation(self, item):
        return World.Resolve(item, Location, self.locations)