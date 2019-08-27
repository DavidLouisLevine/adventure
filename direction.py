class Direction:
    names = ('NORTH', 'SOUTH', 'EAST', 'WEST')
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

    def __init__(self, d):
        if type(d) is str:
            self.d = Direction.FromName(d).d
        else:
            self.d = d

    def Name(self):
        return Direction.names[self.d]

    @staticmethod
    def FromName(name):
        try:
            return Direction(Direction.names.index(name))
        except:
            return None

    @staticmethod
    def IsValid(name):
        return name in Direction.names