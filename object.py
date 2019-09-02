import copy
from direction import Direction
from response import Response

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
            if self.items[i].name == item or self.items[i].abbreviation[:3] == item[:3]:
                if location is None or self.items[i].placement.location == location:
                    return self.items[i]
        return None

    def Add(self, items):
        self.items += items

class Object:
    def __init__(self, name, abbreviation, placement, response=None, moveable=False, visible=True):
        self.name = name
        self.abbreviation = abbreviation
        self.placement = placement
        self.response = response
        self.moveable = moveable
        self.visible = visible

    def Responses(self, iVerb=None):
        if self.response is None:
            responses = ()
        elif type(self.response) is Response:
            responses = (self.response, )
        else:
            responses = self.response

        return filter(lambda x: x.iVerb == iVerb, responses)

    def __str__(self):
        return self.abbreviation

class Action:
    def __init__(self, verb, target):
        self.verb = verb
        self.target = target

def __str__(self):
    return str(self.verb) + ' ' + str(self.target)

class Target:
    def __init__(self, value):
        assert type(value) is Direction or type(value) is Object, "Unknown type: {0}".format(type(value))
        self.value = value

    def IsDirection(self):
        return type(self.value) is Direction

    def IsObject(self):
        return type(self.value) is Object

    def __str__(self):
        return str(self.value)
