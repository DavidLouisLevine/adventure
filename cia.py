# This is a port of the game "C.I.A. Adventure" downloaded from https://www.myabandonware.com/game/cia-adventure-1ya on 2019-08-25
# The description on that site reads:
#   C.I.A. Adventure is a video game published in 1982 on DOS by International PC Owners.
#   It's an adventure game, set in an interactive fiction, spy / espionage and contemporary themes,
#   and was also released on Commodore 64.

from object import Object
from location import NoPlacement
from verb import Verb, BuiltInVerbs
from game import Game, World, State, Response
from direction import *

def GoOpenWoodenDoor(game):
    game.state.location = game.world.locations['CEO']
    return ""

def GoRope(game):
    if game.state.ropeThrown:
        game.state.location = game.world.locations['PIT']
        return ""
    else:
        return None

def GoOpenDoor(game):
    game.state.location = game.world.locations['METAL']

def GoCloset(game):
    game.state.location = game.world.locations['CLOSET']

def GoBuilding(game):
    if game.state.location==game.world.locations['ON A BUSY STREET']:
        game.state.location = game.world.locations['IN THE LOBBY OF THE BUILDING']
        if not game.state.inventory.Has(game.world.objects['BADGE']):
            game.state.location = game.world.locations['IN THE LOBBY OF THE BUILDING']
            return ""
        else:
            m = game.world.verbs['LOOK'].Do(None, game) + '\n'
            m += 'THE DOOR MAN LOOKS AT MY BADGE AND THEN THROWS ME OUT.\n'
            game.state.location = game.world.locations['STREET']
            m += game.world.verbs['LOOK'].Do(None, game)
            return m

def GoDoors(game):
    if game.state.upButtonPushed:
        game.state.location = game.world.locations['ELEVATOR']
        return ""

def GetPainting(game):
    if not game.state.fellFromFrame:
        game.state.fellFromFrame = True
        game.world.objects['CAPSULE']
        return "SOMETHING FELL FROM THE FRAME!"

def GetTelevision(game):
    if not game.state.fellFromFrame:
        game.state.tvConnected = False

def DropCup(game):
    game.state.pillDropped = False
    game.world.object["CUP"].placement = NoPlacement()
    return "I DROPPED THE CUP BUT IT BROKE INTO SMALL PEICES."

def DropGloves(game):
    game.state.glovesWorn = False

def PushUpButton(game):
    game.state.upButtonPushed = True
    return "THE DOORS OPEN WITH A WHOOSH!"

def PushBoxButton(game):
    if game.state.inventory.Has('BOX'):
        m = "I PUSH THE BUTTON ON THE BOX AND\n"
        if game.state.location == game.world.locations['CUBICLE'] or game.state.location == game.world.locations['CONTROL']:
            m += 'THERE IS A BLINDING FLASH....'
            game.state.fl = 1
            game.world.locations['ELEVATOR'].moves[Direction.SOUTH] = 3
            game.state.location = game.world.locations['LOBBY']
        m += "NOTHING HAPPENS."

def PushSquare(game):
    if not game.state.glovesWorn:
        return "THERE'S ELECTRICITY COURSING THRU THE SQUARE!\nI'M BEING ELECTROCUTED!"
    else:
        game.state.boxButtonPushed = True
        return "THE BUTTON ON THE WALL GOES IN .....\nCLICK! SOMETHING SEEMS DIFFFERENT NOW."

def PushElevatorButton(game, floor, locationName):
    if game.state.floor != floor:
        game.state.location.moves[Direction.NORTH] = game.world.locations[locationName].i
        game.state.floor = floor
        return "THE DOORS CLOSE AND I FEEL AS IF THE ROOM IS MOVING.\nSUDDENLY THE DOORS OPEN AGAIN."

def PushOne(game):
    return PushElevatorButton(game, 1, 'IN THE LOBBY OF THE BUILDING')

def PushTwo(game):
    return PushElevatorButton(game, 2, 'IN A SMALL HALLWAY')

def PushThree(game):
    return PushElevatorButton(game, 3, 'IN A SHORT CORRIDOR')

class PushVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            m = target.value.response.f(game)
            if m == "" or m is None:
                m = "NOTHING HAPPENS."
        else:
            m = ""
        return m

class PullVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            m = target.value.response.f(game)
            if m == "" or m is None:
                m = "NOTHING HAPPENS."
        else:
            m = ""
        return m

class WearVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        m = None
        if target.IsObject() and not target.value.response is None:
            m = target.value.response.f(game)
        if m == "" or m is None:
            m = "I CAN'T WEAR THAT!."
        return m

customVerbs = (
    (PushVerb('PUSH', 'PUS')),
    (PullVerb('PULL', 'PUL')),
    (Verb('INSERT', 'INS')),
    (Verb('OPEN', 'OPE')),
    (WearVerb('WEAR', 'WEA', targetInventory=False, targetInRoom=False)),
    (Verb('READ', 'REA')),
    (Verb('STA?', 'STA')),
    (Verb('BREAK?', 'BRE')),
    (Verb('CUT', 'CUT')),
    (Verb('THROW', 'THR')),
    (Verb('CON', 'CON')),
    (Verb('BOND-007-', 'BON')),)

verbs = BuiltInVerbs(customVerbs)

objects = (
    Object('A VIDEO CASSETTE RECORDER', 'REC', 2),
    Object('A VIDEO TAPE', 'TAP', NoPlacement(), moveable=True),
    Object('A LARGE BATTERY', 'BAT', NoPlacement(), moveable=True),
    Object('A BLANK CREDIT CARD', 'CAR', NoPlacement(), moveable=True),
    Object('AN ELECTRONIC LOCK', 'LOC', NoPlacement()),
    Object('AN ELABORATE PAPER WEIGHT', 'WEI', 5, moveable=True),
    Object('A LOCKED WOODEN DOOR', 'DOO', 4),
    Object('AN OPEN WOODEN DOOR', 'DOO', NoPlacement(), Response(1, GoOpenWoodenDoor)),
    Object('A SOLID LOOKING DOOR', 'DOO', 10),
    Object('AN OPEN DOOR', 'DOO', NoPlacement()),
    Object('AN ALERT SECURITY GUARD', 'GUA', 10),
    Object('A SLEEPING SECURITY GUARD', 'GUA', NoPlacement()),
    Object('A LOCKED MAINTENANCE CLOSET', 'CLO', 14),
    Object('A MAINTENANCE CLOSET', 'CLO', NoPlacement(), Response(1, GoCloset)),
    Object('A PLASTIC BAG', 'BAG', 13, moveable=True),
    Object('AN OLDE FASHIONED KEY', 'KEY', 9, moveable=True),
    Object('A SMALL METAL SQUARE ON THE WALL', 'SQU', 16),
    Object('A LEVER ON THE SQUARE', 'LEV', 16),
    Object('AN OLD MAHOGANY DESK', 'DES', 5),
    Object('A BROOM', 'BRO', 13, moveable=True),
    Object('A DUSTPAN', 'DUS', 13, moveable=True),
    Object('A SPIRAL NOTEBOOK', 'NOT', NoPlacement(), moveable=True),
    Object('A MAHOGANY DRAWER', 'DRA', NoPlacement(), moveable=True),
    Object('A GLASS CASE ON A PEDESTAL', 'CAS', 6),
    Object('A RAZOR BLADE', 'BLA', 27, moveable=True),
    Object('A VERY LARGE RUBY', 'RUB', NoPlacement(), moveable=True),
    Object('A SIGN ON THE SQUARE', 'SIG', 16, moveable=True),
    Object('A QUARTER', 'QUA', NoPlacement(), moveable=True),
    Object('A COFFEE MACHINE', 'MAC', 8),
    Object('A CUP OF STEAMING HOT COFFEE', 'CUP', NoPlacement(), Response(3, DropCup), moveable=True),
    Object('A SMALL CAPSULE', 'CAP', NoPlacement(), moveable=True),
    Object('A LARGE SCULPTURE', 'SCU', 3),
    Object('A TALL OFFICE BUILDING', 'BUI', 1, Response(1, GoBuilding)),
    Object('A PAIR OF SLIDING DOORS', 'DOO', 3, Response(1, GoDoors)),
    Object('A LARGE BUTTON ON THE WALL', 'BUT', 29),
    Object('A PANEL OF BUTTONS NUMBERED ONE THRU THREE', 'PAN', 9),
    Object('A STRONG NYLON ROPE', 'ROP', 17, Response(1, GoRope), moveable=True),
    Object('A LARGE HOOK WITH A ROPE HANGING FROM IT', 'HOO', 21),
    Object('A C.I.A. IDENTIFICATION BADGE', 'BAD', NoPlacement(), moveable=True),
    Object('A PORTABLE TELEVISION', 'TEL', 7, moveable=True),
    Object('A BANK OF MONITORS', 'MON', 7),
    Object('A CHAOS I.D. CARD', 'CAR', 30, moveable=True),
    Object('A BANK OF MONITORS', 'MON', 19),
    Object('A SMALL PAINTING', 'PAI', 23, moveable=True),
    Object('A PAIR OF RUBBER GLOVES', 'GLO', 13, Response(3, DropCup), moveable=True),
    Object('A BOX WITH A BUTTON ON IT', 'BOX', 24, moveable=True),
    Object('ONE', 'ONE', 9, Response(1, PushOne), lookable=False),
    Object('TWO', 'TWO', 9, Response(1, PushTwo), lookable=False),
    Object('THREE', 'THR', 9, Response(1, PushThree), lookable=False),
    Object('SLIT', 'SLI', 10, lookable=False),

    # These are not in the original game's object list but are included here
    # so that every target is a direction or an object.
    # In the game, "BUT" is a special cased string when used for this panel.
    Object('AN UP BUTTON', 'BUT', 3, Response(1, PushUpButton), lookable=False),
    Object('A BUTTON ON A BOX', 'BUT', 3, Response(1, PushBoxButton), lookable=False),
    )


class CIA(Game):
    def __init__(self):
        world = World(objects, verbs)
        state =  State(world.locations['ON A BUSY STREET'], world)
        Game.__init__(self, world, state)
        self.state.inventory.Add(world.objects['BADGE'])
        self.state.upButtonPushed = False
        self.state.floor = 1
        self.state.ropeThrown = False
        self.state.glovesWorn = False
        self.state.fellFromFrame = False
        self.state.tvConnected = False
        self.state.pillDropped = False
        self.state.boxButtonPushed = False
        self.combination = 12345
        self.guard_ticks = -1

    def Run(self, actions):
        print("        C.I.A  ADVENTURE")
        self.Do("LOOK", echo=False)
        self.playerName = 'JIM'
        print("ENTER YOUR NAME PARTNER? " + self.playerName)
        print("WRITING ON THE WALL SAYS\nIF YOU WANT INSTRUCTIONS TYPE:ORDERS PLEASE")
        Game.Run(self, sequence)

    def Tick(self):
        if self.guard_ticks != -1:
            self.guard_ticks -= 1

sequence = (
    "GO BUILDING",
    "INVENTORY",
    "WEAR BADGE",
    "DROP BADGE",
    "INVENTORY",
    "LOOK",
    "GO BUILDING",
    "GO WEST",
    "LOOK",
    "GET RECORDER",
    "LOOK",
    "INVENTORY",
    "GO EAST",
    "GO DOORS",
    "PUSH BUTTON",
    "GO DOORS",
    "PUSH TWO",
    "PUSH TWO",
    "GO NORTH")
#sequence = ()

cia = CIA()
cia.Run(sequence)
