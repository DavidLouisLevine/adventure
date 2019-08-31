class Location:
    def __init__(self, abbreviation, name, moves):
        self.name = name
        self.moves = list(moves)
        self.abbreviation = abbreviation

    def __str__(self):
        return self.abbreviation

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
            (Location('VISITOR', 'IN A VISITOR\'S ROOM', (0,  0,  'LOBBY',  0))),
            (Location('LOBBY', 'IN THE LOBBY OF THE BUILDING', ('STREET', 0, 'ANTEROOM', 'VISITOR'))),
            (Location('ANTEROOM', 'IN A DINGY ANTE ROOM', (0, 0, 0, 'LOBBY'))),
            (Location('CEO', 'IN THE COMPANY PRESIDENT\'S OFFICE', (0, 0, 0, 'ANTEROOM'))),
            (Location('CUBICLE', 'IN A SMALL SOUND PROOFED CUBICLE', (0, 'PLAIN', 0, 0))),
            (Location('SECURITY', 'IN A SECURITY OFFICE', (0, 0, 'HALLWAY', 0))),
            (Location('HALLWAY', 'IN A SMALL HALLWAY', (0, 'CAFETERIA', 'ELEVATOR', 'SECURITY'))),
            (Location('ELEVATOR', 'IN A SMALL ROOM', ('LOBBY', 0, 0, 0))),
            (Location('CORRIDOR', 'IN A SHORT CORRIDOR', (0, 'SIDE', 0, 'ELEVATOR'))),
            (Location('METAL', 'IN A HALLWAY MADE OF METAL', (0, 0, 'PLAIN', 'CORRIDOR'))),
            (Location('PLAIN', 'IN A SMALL PLAIN ROOM', ('CUBICLE', 0, 0, 'METAL'))),
            (Location('CLOSET', 'IN A MAINTENANCE CLOSET', (0, 0, 'CAFETERIA', 0))),
            (Location('CAFETERIA', 'IN A CAFETERIA', ('HALLWAY', 0, 0, 0))),
            (Location('SIDE', 'IN A SIDE CORRIDOR', ('CORRIDOR', 0, 'GENERATOR', 0))),
            (Location('GENERATOR', 'IN A POWER GENERATOR ROOM', (0, 0, 0, 'SIDE'))),
            (Location('SUB-BASEMENT', 'IN A SUB-BASEMENT BELOW THE CHUTE', (0, 0, 'COMPLEX', 0))),
            (Location('COMPLEX', 'IN THE ENTRANCE TO THE SECRET COMPLEX', (0, 'LEDGE', 'MONITORING', 'SUB-BASEMENT'))),
            (Location('MONITORING', 'IN A SECRET MONITORING ROOM', (0, 0, 0, 'COMPLEX'))),
            (Location('LEDGE', 'ON A LEDGE IN FRONT OF A METAL PIT 1000\'S OF FEET DEEP', ('COMPLEX', 0, 0, 0))),
            (Location('PIT', 'ON THE OTHER SIDE OF THE PIT', ( 0, 0, 'LONG', 0))),
            (Location('LONG', 'IN A LONG CORRIDOR', (0, 'NARROW', 'ROOM', 'PIT'))),
            (Location('ROOM', 'IN A LARGE ROOM', (0, 'EXAM', 0, 'LONG'))),
            (Location('LAB', 'IN A SECRET LABORATORY', (0, 0, 'NARROW', 0))),
            (Location('NARROW', 'IN A NARROW CROSS CORRIDOR', ('LONG', 0, 0, 'LAB'))),
            (Location('EXAM', 'IN A CROSS EXAMINATION ROOM', ('LARGE', 'CHIEF', 0, 0))),
            (Location('BATHROOM', 'IN A SMALL BATHROOM', (0, 0, 'CHIEF', 0))),
            (Location('CHIEF', 'IN THE OFFICE OF THE CHIEF OF CHAOS', ('EXAM', 'END', 0, 'BATHROOM'))),
            (Location('CONTROL', 'IN THE CHAOS CONTROL ROOM', (0, 0, 'END', 0))),
            (Location('END', 'NEAR THE END OF THE COMPLEX', ('CHIEF', 0, 0, 'CONTROL')))
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