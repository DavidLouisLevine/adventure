# This is a port of the game "C.I.A. Adventure" downloaded from https://www.myabandonware.com/game/cia-adventure-1ya on 2019-08-25
# The description on that site reads:
#   C.I.A. Adventure is a video game published in 1982 on DOS by International PC Owners.
#   It's an adventure game, set in an interactive fiction, spy / espionage and contemporary themes,
#   and was also released on Commodore 64.

from object import Object
from location import NoPlacement
from verb import Verb, BuiltInVerbs, LookAt, CanGet, CantLookAt
from game import Game, World, State
from response import Response
from direction import *

def GoOpenDoor(game, *args, **kwargs):
    game.TravelTo('METAL')

def GoCloset(game, *args, **kwargs):
    game.TravelTo('CLOSET')

def GoBuilding(game, *args, **kwargs):
    if game.state.location==game.world.locations['ON A BUSY STREET']:
#        game.TravelTo('LOBBY')
        if not game.state.inventory.Has(game.world.objects['BADGE']):
            game.TravelTo('LOBBY')
            return ""
        else:
            m = game.Look()
            m += 'THE DOOR MAN LOOKS AT MY BADGE AND THEN THROWS ME OUT.\n'
            game.TravelTo('STREET')
            m += game.Look()
            return m

def GoDoors(game, *args, **kwargs):
    if game.state.upButtonPushed:
        game.TravelTo('ELEVATOR')
        return ""

def GetPainting(game, *args, **kwargs):
    if not game.state.fellFromFrame:
        game.state.fellFromFrame = True
        game.CreateHere('CAPSULE')
        return "SOMETHING FELL FROM THE FRAME!"

def GetTelevision(game, *args, **kwargs):
    if not game.state.fellFromFrame:
        game.state.tvConnected = False

def DropCup(game, *args, **kwargs):
    game.state.pillDropped = False
    game.world.RemoveObject('CUP')
    return "I DROPPED THE CUP BUT IT BROKE INTO SMALL PEICES."

def DropGloves(game, *args, **kwargs):
    game.state.glovesWorn = False

def PushUpButton(game, *args, **kwargs):
    game.state.upButtonPushed = True
    return "THE DOORS OPEN WITH A WHOOSH!"

def PushBoxButton(game, *args, **kwargs):
    if game.state.inventory.Has('BOX'):
        m = "I PUSH THE BUTTON ON THE BOX AND\n"
        if game.state.location == game.world.locations['CUBICLE'] or game.state.location == game.world.locations['CONTROL']:
            m += 'THERE IS A BLINDING FLASH....'
            game.state.floor = 1
            game.world.locations['ELEVATOR'].moves[Direction.SOUTH] = 3
            game.TravelTo('LOBBY')
        m += "NOTHING HAPPENS."

def PushSquare(game, *args, **kwargs):
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

def PushOne(game, *args, **kwargs):
    return PushElevatorButton(game, 1, 'IN THE LOBBY OF THE BUILDING')

def PushTwo(game, *args, **kwargs):
    return PushElevatorButton(game, 2, 'IN A SMALL HALLWAY')

def PushThree(game, *args, **kwargs):
    return PushElevatorButton(game, 3, 'IN A SHORT CORRIDOR')

class PushVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            m = Response.Respond(target.value.response, self.i, game)
            if m == "" or m is None:
                m = "NOTHING HAPPENS."
        else:
            m = ""
        return m

def InsertBattery(game, *args, **kwargs):
    into = game.objects[game.input("TELL ME, IN ONE WORD, INTO WHAT")]
    if into == game.objects['RECORDER']:
        game.state.batteryInserted = True
        game.world.RemoveObject('BATTERY')
        return "OK"

def InsertCard(game, *args, **kwargs):
    into = game.objects[game.input("TELL ME, IN ONE WORD, INTO WHAT")]
    if into == game.objects['SLIT']:
        if game.state.sleepTimer < 0:
            return "THE GUARD WON'T LET ME"
        else:
            game.world.RemoveObject('CARD')
            game.world.MoveObject('LOCK', 'CORRIDOR')
            return "POP! A SECTION OF THE WALL OPENS.....\nREVEALING SOMETHING VERY INTERESTING."

def InsertTape(game, *args, **kwargs):
    into = game.objects[game.input("TELL ME, IN ONE WORD, INTO WHAT")]
    if into == game.objects['RECORDER']:
        game.world.RemoveObject('TAPE')
        return "O.K. THE TAPE IS IN THE RECORDER."

def InsertQuarter(game, *args, **kwargs):
    into = game.objects[game.input("TELL ME, IN ONE WORD, INTO WHAT")]
    if into == game.objects['MACHINE']:
        game.world.RemoveObject('QUARTER')
        game.world.MoveObject('COFFEE', 'HALLWAY')
        return "POP! A CUP OF COFFEE COMES OUT OF THE MACHINE."

def OpenDrawer(game, *args, **kwargs):
    game.state.upButtonPushed = True
    return "THE DOORS OPEN WITH A WHOOSH!"

def OpenWoodenDoor(game, *args, **kwargs):
    if game.Has('KEY'):
        game.world.RemoveObject('A LOCKED WOODEN DOOR')
        game.CreateHere('AN OPEN WOODEN DOOR')
        return "O.K. I OPENED THE DOOR."

class PullVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            m = Response.Respond(target.value.response, self.i, game)
            if m == "" or m is None:
                m = "NOTHING HAPPENS."
        else:
            m = ""
        return m

class InsertVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            if Response.HasResponse(target.value.response, self.i):
                m = Response.Respond(target.value.response, self.i, game)
                if m == "" or m is None:
                    m = "NOTHING HAPPENED."
            else:
                m = "I CAN'T INSERT THAT!"
        else:
            m = ""
        return m

class InsertVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            if Response.HasResponse(target.value.response, self.i):
                m = Response.Respond(target.value.response, self.i, game)
                if m == "" or m is None:
                    m = "NOTHING HAPPENED."
            else:
                m = "I CAN'T INSERT THAT!"
        else:
            m = ""
        return m

class OpenVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            if Response.HasResponse(target.value.response, self.i):
                m = Response.Respond(target.value.response, self.i, game)
                if m == "" or m is None:
                    m = "NOTHING HAPPENED."
            else:
                m = "I CAN'T OPEN THAT!"
        else:
            m = ""
        return m

class WearVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        m = None
        if target.IsObject() and not target.value.response is None:
            m = Response.Respond(target.value.response, self.i, game)
        if m == "" or m is None:
            m = "I CAN'T WEAR THAT!."
        return m

customVerbs = (
    (PushVerb('PUSH', 'PUS')),
    (PullVerb('PULL', 'PUL')),
    (InsertVerb('INSERT', 'INS')),
    (OpenVerb('OPEN', 'OPE')),
    (WearVerb('WEAR', 'WEA', targetInventory=False, targetInRoom=False)),
    (Verb('READ', 'REA')),
    (Verb('STA?', 'STA')),
    (Verb('BREAK?', 'BRE')),
    (Verb('CUT', 'CUT')),
    (Verb('THROW', 'THR')),
    (Verb('CON', 'CON')),
    (Verb('BOND-007-', 'BON')),)

verbs = BuiltInVerbs(customVerbs)
pushResponse = verbs['PUSH'].MakeResponse
goResponse = verbs['GO'].MakeResponse
getResponse = verbs['GET'].MakeResponse
insertResponse = verbs['INSERT'].MakeResponse
openResponse = verbs['OPEN'].MakeResponse
dropResponse = verbs['DROP'].MakeResponse
lookResponse = verbs['LOOK'].MakeResponse

objects = (
    Object('A VIDEO CASSETTE RECORDER', 'REC', 2, (
        lookResponse(LookAt, "THERE'S NO POWER FOR IT.", lambda g: not g.state.batteryInserted),
        lookResponse(LookAt, "THERE'S NO T.V. TO WATCH ON.", lambda g: not g.state.tvConnected))),
    Object('A VIDEO TAPE', 'TAP', NoPlacement(), (
        insertResponse(InsertTape),
        getResponse(CanGet))),
    Object('A LARGE BATTERY', 'BAT', NoPlacement(), (
        insertResponse(InsertBattery),
        getResponse(CanGet))),
    Object('A BLANK CREDIT CARD', 'CAR', NoPlacement(), (
        insertResponse(InsertCard),
        getResponse(CanGet))),
    Object('AN ELECTRONIC LOCK', 'LOC', NoPlacement()),
    Object('AN ELABORATE PAPER WEIGHT', 'WEI', 5, (
        lookResponse(LookAt, "IT LOOKS HEAVY."),
        getResponse(CanGet))),
    Object('A LOCKED WOODEN DOOR', 'DOOR', 4,
           (lookResponse(LookAt, "IT'S LOCKED."),
           (openResponse(OpenWoodenDoor)))),
    Object('AN OPEN WOODEN DOOR', 'DOO', NoPlacement(), goResponse(travelTo='CEO')),
    Object('A SOLID LOOKING DOOR', 'DOO', 10),
    Object('AN OPEN DOOR', 'DOO', NoPlacement()),
    Object('AN ALERT SECURITY GUARD', 'GUA', 10),
    Object('A SLEEPING SECURITY GUARD', 'GUA', NoPlacement()),
    Object('A LOCKED MAINTENANCE CLOSET', 'CLO', 14),
    Object('A MAINTENANCE CLOSET', 'CLO', NoPlacement(), goResponse(GoCloset)),
    Object('A PLASTIC BAG', 'BAG', 13, (
        lookResponse(LookAt, "IT'S A VERY STRONG BAG."),
        getResponse(CanGet))),
    Object('AN OLDE FASHIONED KEY', 'KEY', 9, getResponse(CanGet)),
    Object('A SMALL METAL SQUARE ON THE WALL', 'SQU', 16),
    Object('A LEVER ON THE SQUARE', 'LEV', 16),
    Object('AN OLD MAHOGANY DESK', 'DES', 5, lookResponse(LookAt, "I CAN SEE A LOCKED DRAWER IN IT.")),
    Object('A BROOM', 'BRO', 13, getResponse(CanGet)),
    Object('A DUSTPAN', 'DUS', 13, getResponse(CanGet)),
    Object('A SPIRAL NOTEBOOK', 'NOT', NoPlacement(), (
        lookResponse(LookAt, "THERE'S WRITING ON IT."),
        getResponse(CanGet))),
    Object('A MAHOGANY DRAWER', 'DRA', NoPlacement(), (
        openResponse(OpenDrawer),
        lookResponse(LookAt, "IT LOOKS FRAGILE")),
        getResponse(CanGet)),
    Object('A GLASS CASE ON A PEDESTAL', 'CAS', 6, lookResponse(LookAt, "I CAN SEE A GLEAMING STONE IN IT.")),
    Object('A RAZOR BLADE', 'BLA',
           27, getResponse(CanGet)),
    Object('A VERY LARGE RUBY', 'RUB', NoPlacement(), getResponse(CanGet)),
    Object('A SIGN ON THE SQUARE', 'SIG', 16,
           (lookResponse(LookAt, "THERE'S WRITING ON IT."),
            getResponse(CanGet))),
    Object('A QUARTER', 'QUA', NoPlacement(),
           insertResponse(InsertQuarter),
           getResponse(CanGet)),
    Object('A COFFEE MACHINE', 'MAC', 8),
    Object('A CUP OF STEAMING HOT COFFEE', 'CUP', NoPlacement(), (
        dropResponse(DropCup),
        getResponse(CanGet))),
    Object('A SMALL CAPSULE', 'CAP', NoPlacement(), getResponse(CanGet)),
    Object('A LARGE SCULPTURE', 'SCU', 3),
    Object('A TALL OFFICE BUILDING', 'BUI', 1, goResponse(GoBuilding)),
    Object('A PAIR OF SLIDING DOORS', 'DOO', 3, (
        goResponse(condition=lambda g:g.state.upButtonPushed, travelTo='ELEVATOR'),
        # goResponse(GoDoors),
        lookResponse(LookAt, "THE DOORS ARE OPEN.", lambda g:g.state.upButtonPushed))),
    Object('A LARGE BUTTON ON THE WALL', 'BUT', 29),
    Object('A PANEL OF BUTTONS NUMBERED ONE THRU THREE', 'PAN', 9),
    Object('A STRONG NYLON ROPE', 'ROPE', 17, (
        goResponse(condition=lambda g:g.state.ropeThrown, travelTo= 'PIT'),
        getResponse(CanGet))),
    Object('A LARGE HOOK WITH A ROPE HANGING FROM IT', 'HOO', 21),
    Object('A C.I.A. IDENTIFICATION BADGE', 'BAD', NoPlacement(), getResponse(CanGet)),
    Object('A PORTABLE TELEVISION', 'TEL', 7, getResponse(CanGet)),
    Object('A BANK OF MONITORS', 'MON', 7,
           lookResponse(LookAt, "THE SCREEN IS DARK.", lambda g: not g.state.boxButtonPushed),
           lookResponse(LookAt, "I SEE A METAL PIT 1000'S OF FEET DEEP ON ONE MONITOR.", lambda g: g.state.boxButtonPushed)),
    Object('A CHAOS I.D. CARD', 'CAR', 30, getResponse(CanGet)),
    Object('A BANK OF MONITORS', 'MON', 19),
    Object('A SMALL PAINTING', 'PAI', 23, (
        lookResponse(LookAt, "I SEE A PICTURE OF A GRINNING JACKAL."),
        getResponse(CanGet))),
    Object('A PAIR OF RUBBER GLOVES', 'GLO', 13, (
        dropResponse(DropCup),
        getResponse(CanGet))),
    Object('A BOX WITH A BUTTON ON IT', 'BOX', 24, getResponse(CanGet)),
    Object('ONE', 'ONE', 9, (
        goResponse(PushOne),
        lookResponse(CantLookAt))),
    Object('TWO', 'TWO', 9, (
        goResponse(PushTwo),
        lookResponse(CantLookAt))),
    Object('THREE', 'THR', 9, (
        goResponse(PushThree),
        lookResponse(CantLookAt))),
    Object('SLIT', 'SLI', 10, lookResponse(CantLookAt)),

    # These are not in the original game's object list but are included here
    # so that every target is a direction or an object.
    # In the game, "BUT" is a special cased string when used for this panel.
    Object('AN UP BUTTON', 'BUT', 3, (
        pushResponse(PushUpButton),
        lookResponse(CantLookAt))),
    Object('A BUTTON ON A BOX', 'BUT', 3, (
        goResponse(PushBoxButton),
        lookResponse(CantLookAt))),
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
        self.state.batteryInserted = False
        self.state.tvConnected = False
        self.state.sleepTimer = -1
        self.state.tapeInserted = False
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
sequence = ()

cia = CIA()
cia.Run(sequence)
