# This is a port of the game "C.I.A. Adventure" downloaded from https://www.myabandonware.com/game/cia-adventure-1ya on 2019-08-25
# The description on that site reads:
#   C.I.A. Adventure is a video game published in 1982 on DOS by International PC Owners.
#   It's an adventure game, set in an interactive fiction, spy / espionage and contemporary themes,
#   and was also released on Commodore 64.

# The site at http://gamingafter40.blogspot.com/2013/07/adventure-of-week-cia-adventure-1980.html, downloaded 2019-08-31
# credits the game to Hugh Lampert. That site also has a complete walk through.

from object import Object
from location import NoPlacement
from verb import Verb, BuiltInVerbs, LookAt, CanGet, CantLookAt
from game import Game, World
from response import Response
from direction import *
from state import State

def GoBuilding(game, *args, **kwargs):
    if game.state.location==game.world.locations['ON A BUSY STREET']:
        game.TravelTo('LOBBY')
        if not game.state.inventory.Has(game.world.objects['BADGE']):
            game.TravelTo('LOBBY')
            return ""
        else:
            m = game.Look()
            m += '\nTHE DOOR MAN LOOKS AT MY BADGE AND THEN THROWS ME OUT.\n'
            game.TravelTo('STREET')
            m += game.Look()
            return m

def PushBoxButton(game, *args, **kwargs):
    if game.state.inventory.Has('BOX'):
        m = "I PUSH THE BUTTON ON THE BOX AND\n"
        if game.state.location == game.world.locations['CUBICLE'] or game.state.location == game.world.locations['CONTROL']:
            m += 'THERE IS A BLINDING FLASH....'
            game.state.floor = 1
            game.world.locations['ELEVATOR'].moves[Direction.SOUTH] = 3
            game.TravelTo('LOBBY')
        m += "NOTHING HAPPENS."

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

def ArgStr(kwargs, key):
    return kwargs[key] if key in kwargs else ""

class StandardVerb(Verb):
    def __init__(self, *args, **kwargs):
        self.notApplicableMessage = ArgStr(kwargs, 'notApplicableMessage')
        self.didntWorkMessage = ArgStr(kwargs, 'didntWorkMessage')
        if 'notApplicableMessage' in kwargs:
            self.notApplicableMessage = kwargs.pop('notApplicableMessage')
        if 'didntWorkMessage' in kwargs:
            self.didntWorkMessage = kwargs.pop('didntWorkMessage')
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            if Response.HasResponse(target.value.response, self.i):
                m = Response.Respond(target.value.response, self.i, game)
                if m == "" or m is None:
                    m = self.didntWorkMessage
            else:
                m = self.notApplicableMessage if self.notApplicableMessage is not None else self.didntWorkMessage
        else:
            m = ""
        return m

class PushVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['didntWorkMessage'] = 'NOTHING HAPPENS.'
        StandardVerb.__init__(self, *args, **kwargs)

def OpenDrawer(game, *args, **kwargs):
    pass
    # game.state.upButtonPushed = True
    # return "THE DOORS OPEN WITH A WHOOSH!"

class PullVerb(Verb):
    def __init__(self, *args, **kwargs):
        kwargs['didntWorkMessage'] = 'NOTHING HAPPENS.'
        StandardVerb.__init__(self, *args, **kwargs)

class InsertVerb(Verb):
    def __init__(self, *args, **kwargs):
        kwargs['didntWorkMessage'] = 'NOTHING HAPPENED.'
        StandardVerb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and not target.value.response is None:
            response = Response.get(target.value.response, self.i);
            if response is not None:
                into = game.objects[game.input("TELL ME, IN ONE WORD, INTO WHAT")]
                if into == response.kwargs['insertedObject']:
                    m = Response.Respond(target.value.response, self.i, game)
                    if m == "" or m is None:
                        m = "NOTHING HAPPENED."
            else:
                m = "I CAN'T INSERT THAT!"
        else:
            m = ""
        return m

class OpenVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I CAN'T OPEN THAT!"
        kwargs['didntWorkMessage'] = 'NOTHING HAPPENS.'
        StandardVerb.__init__(self, *args, **kwargs)

class WearVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I CAN'T WEAR THAT!"
        kwargs['didntWorkMessage'] = 'SHOULD NOT SEE THIS MESSAGE'
        StandardVerb.__init__(self, *args, **kwargs)

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
push = verbs['PUSH'].MakeResponse
go = verbs['GO'].MakeResponse
get = verbs['GET'].MakeResponse
insert = verbs['INSERT'].MakeResponse
open = verbs['OPEN'].MakeResponse
drop = verbs['DROP'].MakeResponse
look = verbs['LOOK'].MakeResponse

objects = (
    Object('A VIDEO CASSETTE RECORDER', 'RECORDER', 2, (
        look(LookAt, "THERE'S NO POWER FOR IT.", lambda g: not g.state.batteryInserted),
        look(LookAt, "THERE'S NO T.V. TO WATCH ON.", lambda g: not g.state['tvConnected']))),
    Object('A VIDEO TAPE', 'TAPe', NoPlacement(), (
        insert(into='RECORDER', moveObject='TAPE', message='O.K. THE TAPE IS IN THE RECORDER.'),
       get(CanGet))),
    Object('A LARGE BATTERY', 'BATTERY', NoPlacement(), (
        insert(into='RECORDER', setState=('batteryInserted', True), removeObject='BATTERY', message='OK'),
        get(CanGet))),
    Object('A BLANK CREDIT CARD', 'CARD', NoPlacement(), (
        insert(into='SLIT', condition=lambda g: g.state.sleepTimer < 0, messsage="THE GUARD WON'T LET ME"),
        insert(into='SLIT', condition=lambda g: g.state.sleepTimer >= 0, removeObject='CARD', moveObject = ('LOCK', 'CORRIDOR'), message='POP! A SECTION OF THE WALL OPENS.....\nREVEALING SOMETHING VERY INTERESTING.'),
        get(CanGet))),
    Object('AN ELECTRONIC LOCK', 'LOCK', NoPlacement()),
    Object('AN ELABORATE PAPER WEIGHT', 'WEIGHT', 5, (
        look(LookAt, "IT LOOKS HEAVY."),
        get(CanGet))),
    Object('A LOCKED WOODEN DOOR', 'DOOR', 4,
       (look(LookAt, "IT'S LOCKED."),
       (open(condition=lambda g:g.Has('KEY'), replaceObject=('A LOCKED WOODEN DOOR', 'AN OPEN WOODEN DOOR'), message='O.K. I OPENED THE DOOR.')))),
    Object('AN OPEN WOODEN DOOR', 'DOOR', NoPlacement(), go(travelTo='CEO')),
    Object('A SOLID LOOKING DOOR', 'DOOR', 10),
    Object('AN OPEN DOOR', 'DOOR', NoPlacement(), go(travelTo='METAL')),
    Object('AN ALERT SECURITY GUARD', 'GUARD', 10),
    Object('A SLEEPING SECURITY GUARD', 'GUARD', NoPlacement()),
    Object('A LOCKED MAINTENANCE CLOSET', 'CLOSET', 14),
    Object('A MAINTENANCE CLOSET', 'CLOSET', NoPlacement(), go(travelTo='CLOSET')),
    Object('A PLASTIC BAG', 'BAG', 13, (
        look(LookAt, "IT'S A VERY STRONG BAG."),
        get(CanGet))),
    Object('AN OLDE FASHIONED KEY', 'KEY', 9, get(CanGet)),
    Object('A SMALL METAL SQUARE ON THE WALL', 'SQUARE', 16,
        push(condition=lambda g:g.state['glovesWorn'], setState=('boxButtonPushed', True), message="THE BUTTON ON THE WALL GOES IN .....\nCLICK! SOMETHING SEEMS DIFFFERENT NOW."),
        push(isFatal=True, message="THERE'S ELECTRICITY COURSING THRU THE SQUARE!\nI'M BEING ELECTROCUTED!")),
    Object('A LEVER ON THE SQUARE', 'LEVER', 16),
    Object('AN OLD MAHOGANY DESK', 'DESK', 5, look(LookAt, "I CAN SEE A LOCKED DRAWER IN IT.")),
    Object('A BROOM', 'BROOM', 13, get(CanGet)),
    Object('A DUSTPAN', 'DUSTPAN', 13, get(CanGet)),
    Object('A SPIRAL NOTEBOOK', 'NOTEBOOK', NoPlacement(), (
        look(LookAt, "THERE'S WRITING ON IT."),
        get(CanGet))),
    Object('A MAHOGANY DRAWER', 'DRAWER', 5, (
        open(OpenDrawer),
        look(LookAt, "IT LOOKS FRAGILE")),
        get(CanGet)),
    Object('A GLASS CASE ON A PEDESTAL', 'CASE', 6, look(LookAt, "I CAN SEE A GLEAMING STONE IN IT.")),
    Object('A RAZOR BLADE', 'BLADE',
           27, get(CanGet)),
    Object('A VERY LARGE RUBY', 'RUBY', NoPlacement(), get(CanGet)),
    Object('A SIGN ON THE SQUARE', 'SIGN', 16,
           (look(message="THERE'S WRITING ON IT."),
            get(CanGet))),
    Object('A QUARTER', 'QUARTER', NoPlacement(),
           insert(into='MACHINE', moveObject=('COFFEE', 'HALLWAY'), message='POP! A CUP OF COFFEE COMES OUT OF THE MACHINE.'),
           get(CanGet)),
    Object('A COFFEE MACHINE', 'MACHINE', 8),
    Object('A CUP OF STEAMING HOT COFFEE', 'CUP', NoPlacement(), (
        drop(setState=('pillDropped', False), removeObject='CUP', message='I DROPPED THE CUP BUT IT BROKE INTO SMALL PEICES.'),
        get(CanGet))),
    Object('A SMALL CAPSULE', 'CAPSULE', NoPlacement(), get(CanGet)),
    Object('A LARGE SCULPTURE', 'SCULPTURE', 3),
    Object('A TALL OFFICE BUILDING', 'BUILDING', 1, go(GoBuilding)),
    Object('A PAIR OF SLIDING DOORS', 'DOORS', 3, (
        go(condition=lambda g:g.state['upButtonPushed'], travelTo='ELEVATOR'),
        look(LookAt, "THE DOORS ARE OPEN.", lambda g:g.state['upButtonPushed']))),
    Object('A LARGE BUTTON ON THE WALL', 'BUTTON', 29),
    Object('A PANEL OF BUTTONS NUMBERED ONE THRU THREE', 'PANEL', 9),
    Object('A STRONG NYLON ROPE', 'ROPE', 17, (
        go(condition=lambda g:g.state.ropeThrown, travelTo= 'PIT'),
        get(CanGet))),
    Object('A LARGE HOOK WITH A ROPE HANGING FROM IT', 'HOOK', 21),
    Object('A C.I.A. IDENTIFICATION BADGE', 'BADGE', NoPlacement(), get(CanGet)),
    Object('A PORTABLE TELEVISION', 'TELEVISION', 7, get(CanGet, setState=('tvConnected', True))),
    Object('A BANK OF MONITORS', 'MONITORS', 7,
           look(LookAt, "THE SCREEN IS DARK.", lambda g: not g.state.boxButtonPushed),
           look(LookAt, "I SEE A METAL PIT 1000'S OF FEET DEEP ON ONE MONITOR.", lambda g: g.state.boxButtonPushed)),
    Object('A CHAOS I.D. CARD', 'CARD', 30, get(CanGet)),
    Object('A BANK OF MONITORS', 'MONITORS', 19),
    Object('A SMALL PAINTING', 'PAINTING', 23, (
        look(LookAt, "I SEE A PICTURE OF A GRINNING JACKAL."),
        get(setState=('fellFromFrame', True), createHere='CAPSULE', message='SOMETHING FELL FROM THE FRAME!'))),
    Object('A PAIR OF RUBBER GLOVES', 'GLOVES', 13, (
        drop(setState=('glovesWorn', False)),
        get(CanGet))),
    Object('A BOX WITH A BUTTON ON IT', 'BOX', 24, get(CanGet)),
    Object('ONE', 'ONE', 9, (
        go(PushOne),
        look(CantLookAt))),
    Object('TWO', 'TWO', 9, (
        go(PushTwo),
        look(CantLookAt))),
    Object('THREE', 'THR', 9, (
        go(PushThree),
        look(CantLookAt))),
    Object('SLIT', 'SLI', 10, look(CantLookAt)),

    # These are not in the original game's object list but are included here
    # so that every target is a direction or an object.
    # In the game, "BUT" is a special cased string when used for this panel.
    Object('AN UP BUTTON', 'BUTTON', 3, (
        push(setState=('upButtonPushed', True), message='THE DOORS OPEN WITH A WHOOSH!'),
        look(CantLookAt))),
    Object('A BUTTON ON A BOX', 'BUTTON', 3, (
        go(PushBoxButton),
        look(CantLookAt))),
)

class CIA(Game):
    def __init__(self):
        world = World(objects, verbs)
        state =  State(world.locations['ON A BUSY STREET'], world)
        Game.__init__(self, world, state)
        self.state.inventory.Add(world.objects['BADGE'])
        self.state['upButtonPushed'] = False
        self.state.floor = 1
        self.state.ropeThrown = False
        self.state['glovesWorn'] = False
        self.state['fellFromFrame'] = False
        self.state.pillDropped = False
        self.state.boxButtonPushed = False
        self.state.batteryInserted = False
        self.state['tvConnected'] = False
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
