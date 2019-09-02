from adventure.direction import Direction
from adventure.placement import NoPlacement
from adventure.object import Object
from adventure.verb import CanGet
from cia.cia_verb import verbs

def GoBuilding(game, *args, **kwargs):
    if game.state.location==game.world.locations['ON A BUSY STREET']:
        game.TravelTo('LOBBY')
        if not game.Has('BADGE'):
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

push = verbs['PUSH'].MakeResponse
go = verbs['GO'].MakeResponse
get = verbs['GET'].MakeResponse
insert = verbs['INSERT'].MakeResponse
open = verbs['OPEN'].MakeResponse
drop = verbs['DROP'].MakeResponse
look = verbs['LOOK'].MakeResponse
objects = (
    Object('A VIDEO CASSETTE RECORDER', 'RECORDER', 'VISITOR', (
        look(conditionIsNotSet='batteryInserted', message="THERE'S NO POWER FOR IT."),
        look(conditionIsNotSet='tvConnected', message="THERE'S NO T.V. TO WATCH ON."))),
    Object('A VIDEO TAPE', 'TAPE', NoPlacement(), (
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
    Object('AN ELABORATE PAPER WEIGHT', 'WEIGHT', 'CEO', (
        look(message="IT LOOKS HEAVY."),
        get(CanGet))),
    Object('A LOCKED WOODEN DOOR', 'DOOR', 'ANTEROOM',
       (look(message="IT'S LOCKED."),
       (open(conditionHas='KEY', replaceObject=('A LOCKED WOODEN DOOR', 'AN OPEN WOODEN DOOR'), message='O.K. I OPENED THE DOOR.')))),
    Object('AN OPEN WOODEN DOOR', 'DOOR', NoPlacement(), go(travelTo='CEO')),
    Object('A SOLID LOOKING DOOR', 'DOOR', 'CORRIDOR', open(message="I CAN'T. IT DOESN'T WORK.")),
    Object('AN OPEN DOOR', 'DOOR', NoPlacement(), go(travelTo='METAL')),
    Object('AN ALERT SECURITY GUARD', 'GUARD', 'CORRIDOR'),
    Object('A SLEEPING SECURITY GUARD', 'GUARD', NoPlacement()),
    Object('A LOCKED MAINTENANCE CLOSET', 'CLOSET', 'CAFETERIA',
        (look(message="IT'S LOCKED."),
        (open(conditionHas='KEY', replaceObject=('A LOCKED MAINTENANCE CLOSET', 'A MAINTENANCE CLOSET'), message='O.K. I OPENED THE DOOR.')))),
    Object('A MAINTENANCE CLOSET', 'CLOSET', NoPlacement(), go(travelTo='CLOSET')),
    Object('A PLASTIC BAG', 'BAG', 13, (
        look(message="IT'S A VERY STRONG BAG."),
        get(CanGet))),
    Object('AN OLDE FASHIONED KEY', 'KEY', 'ELEVATOR', get(CanGet)),
    Object('A SMALL METAL SQUARE ON THE WALL', 'SQUARE', 'GENERATOR',
        push(conditionIsSet='glovesWorn', setState=('boxButtonPushed', True), message="THE BUTTON ON THE WALL GOES IN .....\nCLICK! SOMETHING SEEMS DIFFFERENT NOW."),
        push(isFatal=True, message="THERE'S ELECTRICITY COURSING THRU THE SQUARE!\nI'M BEING ELECTROCUTED!")),
    Object('A LEVER ON THE SQUARE', 'LEVER', 'GENERATOR'),
    Object('AN OLD MAHOGANY DESK', 'DESK', 'CEO', look(message="I CAN SEE A LOCKED DRAWER IN IT.")),
    Object('A BROOM', 'BROOM', 'CLOSET', get(CanGet)),
    Object('A DUSTPAN', 'DUSTPAN', 'CLOSET', get(CanGet)),
    Object('A SPIRAL NOTEBOOK', 'NOTEBOOK', NoPlacement(), (
        look(message="THERE'S WRITING ON IT."),
        get(CanGet))),
    Object('A MAHOGANY DRAWER', 'DRAWER', 'CEO', (
        open(conditionHas='WEIGHT', message="IT'S STUCK"),
        open(message="IT's STUCK"), # Lowercase 's' in original code
        look(message="IT LOOKS FRAGILE")),
        get(CanGet),
        visible=False),
    Object('A GLASS CASE ON A PEDESTAL', 'CASE', 'CUBICLE', look(message="I CAN SEE A GLEAMING STONE IN IT.")),
    Object('A RAZOR BLADE', 'BLADE',
           27, get(CanGet)),
    Object('A VERY LARGE RUBY', 'RUBY', NoPlacement(), get(CanGet)),
    Object('A SIGN ON THE SQUARE', 'SIGN', 'GENERATOR',
           (look(message="THERE'S WRITING ON IT."),
            get(CanGet))),
    Object('A QUARTER', 'QUARTER', NoPlacement(),
           insert(into='MACHINE', moveObject=('COFFEE', 'HALLWAY'), message='POP! A CUP OF COFFEE COMES OUT OF THE MACHINE.'),
           get(CanGet)),
    Object('A COFFEE MACHINE', 'MACHINE', 'HALLWAY'),
    Object('A CUP OF STEAMING HOT COFFEE', 'CUP', NoPlacement(), (
        drop(setState=('pillDropped', False), removeObject='CUP', message='I DROPPED THE CUP BUT IT BROKE INTO SMALL PEICES.'),
        get(CanGet))),
    Object('A SMALL CAPSULE', 'CAPSULE', NoPlacement(), get(CanGet)),
    Object('A LARGE SCULPTURE', 'SCULPTURE', 'LOBBY'),
    Object('A TALL OFFICE BUILDING', 'BUILDING', 1, go(GoBuilding)),
    Object('A PAIR OF SLIDING DOORS', 'DOORS', 'LOBBY', (
        go(conditionIsSet='upButtonPushed', travelTo='ELEVATOR'),
        look(conditionIsSet='upButtonPushed', message="THE DOORS ARE OPEN."))),
    Object('A LARGE BUTTON ON THE WALL', 'BUTTON', 'CONTROL'),
    Object('A PANEL OF BUTTONS NUMBERED ONE THRU THREE', 'PANEL', 'ELEVATOR'),
    Object('A STRONG NYLON ROPE', 'ROPE', 'SUB-BASEMENT', (
        go(conditionIsSet='ropeThrown', travelTo= 'PIT'),
        get(CanGet))),
    Object('A LARGE HOOK WITH A ROPE HANGING FROM IT', 'HOOK', 'PIT'),
    Object('A C.I.A. IDENTIFICATION BADGE', 'BADGE', NoPlacement(), get(CanGet)),
    Object('A PORTABLE TELEVISION', 'TELEVISION', 7, get(CanGet, setState=('tvConnected', True))),
    Object('A BANK OF MONITORS', 'MONITORS', 'SECURITY',
           look(conditinNotSet='boxButtonPushed', message="THE SCREEN IS DARK."),
           look(message="I SEE A METAL PIT 1000'S OF FEET DEEP ON ONE MONITOR.")),
    Object('A CHAOS I.D. CARD', 'CARD', 'END', get(CanGet)),
    Object('A BANK OF MONITORS', 'MONITORS', 'MONITORING'),
    Object('A SMALL PAINTING', 'PAINTING', 'ROOM', (
        look(message="I SEE A PICTURE OF A GRINNING JACKAL."),
        get(setState=('fellFromFrame', True), createHere='CAPSULE', message='SOMETHING FELL FROM THE FRAME!'))),
    Object('A PAIR OF RUBBER GLOVES', 'GLOVES', 'CLOSET', (
        drop(setState=('glovesWorn', False)),
        get(CanGet))),
    Object('A BOX WITH A BUTTON ON IT', 'BOX', 'LAB', get(CanGet)),
    Object('ONE', 'ONE', 'ELEVATOR', go(PushOne), visible=False),
    Object('TWO', 'TWO', 'ELEVATOR', go(PushTwo), visible=False),
    Object('THREE', 'THR', 'ELEVATOR', go(PushThree), visible=False),
    Object('SLIT', 'SLI', 'CORRIDOR', visible=False),

    # These are not in the original game's object list but are included here
    # so that every target is a direction or an object.
    # In the game, "BUT" is a special cased string when used for this panel.
    Object('AN UP BUTTON', 'BUTTON', 3, push(setState=('upButtonPushed', True), message='THE DOORS OPEN WITH A WHOOSH!'), visible=False),
    Object('A BUTTON ON A BOX', 'BUTTON', 3, go(PushBoxButton), visible=False),
)