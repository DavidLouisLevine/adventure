class Location:
    def __init__(self, name, moves):
        self.name = name
        self.moves = moves

class Placement:
    def InInventory(self):
        return self.inventory

    def Exists(self):
        return self.exists

class PlacementLocation(Placement):
    def __init__(self, location):
        #self.location = Location(location)
        self.location = location
        self.inventory = False
        self.exists = True

    def __str__(self):
        return self.location.name

class InventoryLocation(Placement):
    def __init__(self):
        self.location = None
        self.inventory = True
        self.exists = True

    def __str__(self):
        return 'Inventory'

class NoLocation(Placement):
    def __init__(self):
        self.location = None
        self.inventory = False
        self.exists = None

    def __str__(self):
        return "Doesn't exist"


class Locations:
    def __init__(self):
        self.items = (
            (Location('ON A BUSY STREET', (0, 0, 0, 0))),
            (Location('IN A VISITOR\'S ROOM', (0,  0,  3,  0))),
            (Location('IN THE LOBBY OF THE BUILDING', (1, 0, 4, 2))),
            (Location('IN A DINGY ANTE ROOM', (0, 0, 0, 3))),
            (Location('IN THE COMPANY PRESIDENT\'S OFFICE', (0, 0, 0, 4 ))),
            (Location('IN A SMALL SOUND PROOFED CUBICLE', (0, 12, 0, 0))),
            (Location('IN A SECURITY OFFICE', (0, 0, 8, 0))),
            (Location('IN A SMALL HALLWAY', (0, 14, 9, 7))),
            (Location('IN A SMALL ROOM', (3, 0, 0, 0))),
            (Location('IN A SHORT CORRIDOR', (0, 15, 0, 9))),
            (Location('IN A HALLWAY MADE OF METAL', (0, 0, 12, 10))),
            (Location('IN A SMALL PLAIN ROOM', (6, 0, 0, 11))),
            (Location('IN A MAINTENANCE CLOSET', (0, 0, 14, 0))),
            (Location('IN A CAFETERIA', (8, 0, 0, 0))),
            (Location('IN A SIDE CORRIDOR', (10, 0, 16, 0))),
            (Location('IN A POWER GENERATOR ROOM', (0, 0, 0, 15))),
            (Location('IN A SUB-BASEMENT BELOW THE CHUTE', (0, 0, 18, 0))),
            (Location('IN THE ENTRANCE TO THE SECRET COMPLEX', (0, 20, 19, 17))),
            (Location('IN A SECRET MONITORING ROOM', (0, 0, 0, 18))),
            (Location('ON A LEDGE IN FRONT OF A METAL PIT 1000\'S OF FEET DEEP', ( 18 ,  0 ,  0 ,  0 ))),
            (Location('ON THE OTHER SIDE OF THE PIT', ( 0, 0, 22, 0))),
            (Location('IN A LONG CORRIDOR', (0, 25, 23, 21))),
            (Location('IN A LARGE ROOM', (0, 26, 0, 22))),
            (Location('IN A SECRET LABORATORY', (0, 0, 25, 0))),
            (Location('IN A NARROW CROSS CORRIDOR', (22, 0, 0, 24))),
            (Location('IN A CROSS EXAMINATION ROOM', (23, 28, 0, 0))),
            (Location('IN A SMALL BATHROOM', (0, 0, 28, 0))),
            (Location('IN THE OFFICE OF THE CHIEF OF CHAOS', (26, 30, 0, 27))),
            (Location('IN THE CHAOS CONTROL ROOM', (0, 0, 30, 0))),
            (Location('NEAR THE END OF THE COMPLEX', (28, 0, 0, 29)))
        )

    def len(self):
        return len(self.items)

    def __getitem__(self, item):
        if type(item) is str:
            for i in range(len(self.items)):
                if self.items[i].name == item:
                    return self.items[i]
            return None
        else:
            return self.items[item - 1]