class Location:
    def __init__(self, abbreviation, name, moves):
        self.name = name
        self.moves = list(moves)
        self.abbreviation = abbreviation

class Placement:
    def InInventory(self):
        return self.inventory

    def Exists(self):
        return self.exists

class LocationPlacement(Placement):
    def __init__(self, location):
        self.location = location
        self.inventory = False
        self.exists = True

    def __str__(self):
        return self.location.name

class InventoryPlacement(Placement):
    def __init__(self):
        self.location = None
        self.inventory = True
        self.exists = True

    def __str__(self):
        return 'Inventory'

class NoPlacement(Placement):
    def __init__(self):
        self.location = None
        self.inventory = False
        self.exists = None

    def __str__(self):
        return "Doesn't exist"

class Locations:
    def __init__(self):
        self.items = (
            (Location('STREET', 'ON A BUSY STREET', (0, 0, 0, 0))),
            (Location('VISITOR', 'IN A VISITOR\'S ROOM', (0,  0,  3,  0))),
            (Location('LOBBY', 'IN THE LOBBY OF THE BUILDING', (1, 0, 4, 2))),
            (Location('ANTE', 'IN A DINGY ANTE ROOM', (0, 0, 0, 3))),
            (Location('CEO', 'IN THE COMPANY PRESIDENT\'S OFFICE', (0, 0, 0, 4 ))),
            (Location('CUBICLE', 'IN A SMALL SOUND PROOFED CUBICLE', (0, 12, 0, 0))),
            (Location('SECURITY', 'IN A SECURITY OFFICE', (0, 0, 8, 0))),
            (Location('HALLWAY', 'IN A SMALL HALLWAY', (0, 14, 9, 7))),
            (Location('ELEVATOR', 'IN A SMALL ROOM', (3, 0, 0, 0))),
            (Location('CORRIDOR', 'IN A SHORT CORRIDOR', (0, 15, 0, 9))),
            (Location('METAL', 'IN A HALLWAY MADE OF METAL', (0, 0, 12, 10))),
            (Location('PLAIN', 'IN A SMALL PLAIN ROOM', (6, 0, 0, 11))),
            (Location('CLOSET', 'IN A MAINTENANCE CLOSET', (0, 0, 14, 0))),
            (Location('CAFETERIA', 'IN A CAFETERIA', (8, 0, 0, 0))),
            (Location('SIDE', 'IN A SIDE CORRIDOR', (10, 0, 16, 0))),
            (Location('GENERATOR', 'IN A POWER GENERATOR ROOM', (0, 0, 0, 15))),
            (Location('SUB-BASEMENT', 'IN A SUB-BASEMENT BELOW THE CHUTE', (0, 0, 18, 0))),
            (Location('COMPLEX', 'IN THE ENTRANCE TO THE SECRET COMPLEX', (0, 20, 19, 17))),
            (Location('MONITORING', 'IN A SECRET MONITORING ROOM', (0, 0, 0, 18))),
            (Location('LEDGE', 'ON A LEDGE IN FRONT OF A METAL PIT 1000\'S OF FEET DEEP', ( 18 ,  0 ,  0 ,  0 ))),
            (Location('PIT', 'ON THE OTHER SIDE OF THE PIT', ( 0, 0, 22, 0))),
            (Location('LONG', 'IN A LONG CORRIDOR', (0, 25, 23, 21))),
            (Location('ROOM', 'IN A LARGE ROOM', (0, 26, 0, 22))),
            (Location('LAB', 'IN A SECRET LABORATORY', (0, 0, 25, 0))),
            (Location('NARROW', 'IN A NARROW CROSS CORRIDOR', (22, 0, 0, 24))),
            (Location('EXAM', 'IN A CROSS EXAMINATION ROOM', (23, 28, 0, 0))),
            (Location('BATHROOM', 'IN A SMALL BATHROOM', (0, 0, 28, 0))),
            (Location('CHIEF', 'IN THE OFFICE OF THE CHIEF OF CHAOS', (26, 30, 0, 27))),
            (Location('CHAOS', 'IN THE CHAOS CONTROL ROOM', (0, 0, 30, 0))),
            (Location('END', 'NEAR THE END OF THE COMPLEX', (28, 0, 0, 29)))
        )
        for i in range(len(self.items)):
            self.items[i].i = i + 1

    def len(self):
        return len(self.items)

    def __getitem__(self, item):
        if type(item) is str:
            for i in range(len(self.items)):
                if self.items[i].name == item or self.items[i].abbreviation[:3] == item[:3]:
                    return self.items[i]
            return None
        else:
            return self.items[item - 1]