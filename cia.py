# This is a port of the game "C.I.A. Adventure" downloaded from https://www.myabandonware.com/game/cia-adventure-1ya on 2019-08-25
# The description on that site reads:
#   C.I.A. Adventure is a video game published in 1982 on DOS by International PC Owners.
#   It's an adventure game, set in an interactive fiction, spy / espionage and contemporary themes,
#   and was also released on Commodore 64.

from object import Object
from location import NoLocation
from verb import Verb, ObjectVerb, BuiltInVerbs
from game import Game, World, State, Response
from direction import *

def GoBuilding(state, world):
    if state.location==world.locations['ON A BUSY STREET']:
        if not state.inventory.Has(world.objects['BADGE']):
            state.location = world.locations['IN THE LOBBY OF THE BUILDING']
        else:
            return 'THE GUARD LOOKS AT ME SUSPICIOUSLY, THEN THROWS ME BACK.'

def GoDoors(state, world):
    if state.location==world.locations['IN THE LOBBY OF THE BUILDING'] and state.upButtonPushed:
        state.location = world.locations['IN A SMALL ROOM']
        return ""

def PushUp(state, world):
    state.upButtonPushed = True
    return "THE DOORS OPEN WITH A WHOOSH!"

def PushElevatorButton(state, world, floor, locationName):
    if state.floor != floor:
        state.location.moves[Direction.NORTH] = world.locations[locationName].i
        state.floor = floor
        return "THE DOORS CLOSE AND I FEEL AS IF THE ROOM IS MOVING.\nSUDDENLY THE DOORS OPEN AGAIN."

def PushOne(state, world):
    return PushElevatorButton(state, world, 1, 'IN THE LOBBY OF THE BUILDING')

def PushTwo(state, world):
    return PushElevatorButton(state, world, 2, 'IN A SMALL HALLWAY')

def PushThree(state, world):
    return PushElevatorButton(state, world, 3, 'IN A SHORT CORRIDOR')

class PushVerb(ObjectVerb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            return target.value.response.f(game.state, game.world)
        else:
            return ""

verbs = (
    (PushVerb('PUSH', 'PUS')),
    (Verb('PULL', 'PUL')),
    (Verb('INSERT', 'INS')),
    (Verb('OPEN', 'OPE')),
    (Verb('WEAR', 'WEA')),
    (Verb('READ', 'REA')),
    (Verb('STA?', 'STA')),
    (Verb('BREAK?', 'BRE')),
    (Verb('CUT', 'CUT')),
    (Verb('THROW', 'THR')),
    (Verb('CON', 'CON')),
    (Verb('BOND-007-', 'BON')),
)

builtInVerbs = BuiltInVerbs(verbs)

objects = (
    Object('A VIDEO CASSETTE RECORDER', 'REC', 2),
    Object('A VIDEO TAPE', 'TAP', NoLocation(), moveable=True),
    Object('A LARGE BATTERY', 'BAT', NoLocation(), moveable=True),
    Object('A BLANK CREDIT CARD', 'CAR', NoLocation(), moveable=True),
    Object('AN ELECTRONIC LOCK', 'LOC', NoLocation()),
    Object('AN ELABORATE PAPER WEIGHT', 'WEI', 5, moveable=True),
    Object('A LOCKED WOODEN DOOR', 'DOO', 4),
    Object('AN OPEN WOODEN DOOR', 'DOO', NoLocation()),
    Object('A SOLID LOOKING DOOR', 'DOO', 10),
    Object('AN OPEN DOOR', 'DOO', NoLocation()),
    Object('AN ALERT SECURITY GUARD', 'GUA', 10),
    Object('A SLEEPING SECURITY GUARD', 'GUA', NoLocation()),
    Object('A LOCKED MAINTENANCE CLOSET', 'CLO', 14),
    Object('A MAINTENANCE CLOSET', 'CLO', NoLocation()),
    Object('A PLASTIC BAG', 'BAG', 13, moveable=True),
    Object('AN OLDE FASHIONED KEY', 'KEY', 9, moveable=True),
    Object('A SMALL METAL SQUARE ON THE WALL', 'SQU', 16),
    Object('A LEVER ON THE SQUARE', 'LEV', 16),
    Object('AN OLD MAHOGANY DESK', 'DES', 5),
    Object('A BROOM', 'BRO', 13, moveable=True),
    Object('A DUSTPAN', 'DUS', 13, moveable=True),
    Object('A SPIRAL NOTEBOOK', 'NOT', NoLocation(), moveable=True),
    Object('A MAHOGANY DRAWER', 'DRA', NoLocation(), moveable=True),
    Object('A GLASS CASE ON A PEDESTAL', 'CAS', 6),
    Object('A RAZOR BLADE', 'BLA', 27, moveable=True),
    Object('A VERY LARGE RUBY', 'RUB', NoLocation(), moveable=True),
    Object('A SIGN ON THE SQUARE', 'SIG', 16, moveable=True),
    Object('A QUARTER', 'QUA', NoLocation(), moveable=True),
    Object('A COFFEE MACHINE', 'MAC', 8),
    Object('A CUP OF STEAMING HOT COFFEE', 'CUP', NoLocation(), moveable=True),
    Object('A SMALL CAPSULE', 'CAP', NoLocation(), moveable=True),
    Object('A LARGE SCULPTURE', 'SCU', 3),
    Object('A TALL OFFICE BUILDING', 'BUI', 1, Response(1, GoBuilding)),
    Object('A PAIR OF SLIDING DOORS', 'DOO', 3, Response(1, GoDoors)),
    Object('A LARGE BUTTON ON THE WALL', 'BUT', 29),
    Object('A PANEL OF BUTTONS NUMBERED ONE THRU THREE', 'PAN', 9),
    Object('A STRONG NYLON ROPE', 'ROP', 17, moveable=True),
    Object('A LARGE HOOK WITH A ROPE HANGING FROM IT', 'HOO', 21),
    Object('A C.I.A. IDENTIFICATION BADGE', 'BAD', NoLocation(), moveable=True),
    Object('A PORTABLE TELEVISION', 'TEL', 7, moveable=True),
    Object('A BANK OF MONITORS', 'MON', 7),
    Object('A CHAOS I.D. CARD', 'CAR', 30, moveable=True),
    Object('A BANK OF MONITORS', 'MON', 19),
    Object('A SMALL PAINTING', 'PAI', 23, moveable=True),
    Object('A PAIR OF RUBBER GLOVES', 'GLO', 13, moveable=True),
    Object('A BOX WITH A BUTTON ON IT', 'BOX', 24, moveable=True),
    Object('ONE', 'ONE', 9, Response(1, PushOne), lookable=False),
    Object('TWO', 'TWO', 9, Response(1, PushTwo), lookable=False),
    Object('THREE', 'THR', 9, Response(1, PushThree), lookable=False),
    Object('SLIT', 'SLI', 10, lookable=False),

    # These are not in the original game's object list but are included here
    # so that every target is a direction or an object.
    # In the game, "BUT" is a special cased string when used for this panel.
    Object('A PANEL WITH ONE BUTTON', 'BUT', 3, Response(1, PushUp), lookable=False),
    )

world = World(objects, builtInVerbs)

game = Game(world, State(world.locations['ON A BUSY STREET'], world))
game.state.inventory.Add(world.objects['BADGE'])
game.state.upButtonPushed = False
game.state.floor = 1

game.Do("GO BUILDING")
game.Do("INVENTORY")
game.Do("DROP BADGE")
game.Do("INVENTORY")
game.Do("LOOK")
game.Do("GO BUILDING")
game.Do("GO WEST")
game.Do("LOOK")
game.Do("GET RECORDER")
game.Do("LOOK")
game.Do("INVENTORY")
game.Do("GO EAST")
game.Do("GO DOORS")
game.Do("PUSH BUTTON")
game.Do("GO DOORS")
game.Do("PUSH TWO")
game.Do("GO NORTH")
