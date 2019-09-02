from adventure.direction import Direction
from adventure.object import Object

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