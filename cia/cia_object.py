from adventure.placement import NoPlacement
from adventure.object import Object
from adventure.response import Response
from cia.cia_verb import push, pull, go, get, insert, open, drop, wear, read, start, break_, cut, throw, connect, look

objects = (
    Object('A VIDEO CASSETTE RECORDER', 'RECORDER', 'VISITOR', (
        look(ifNotSet='batteryInserted', message="THERE'S NO POWER FOR IT.", result=Response.NotUseful),
        look(ifNotSet='tvConnected', message="THERE'S NO T.V. TO WATCH ON.", result=Response.NotUseful),
        start(ifSet=('batteryInserted', 'tapeInserted', 'tvConnected'),
              setState=('sculptureMessage', True),
              message="{playerName},\nWE HAVE UNCOVERED A NUMBER THAT MAY HELP YOU.\nTHAT NUMBER IS:{secretCode}. PLEASE WATCH OUT FOR HIDDEN TRAPS.\nALSO, THERE IS SOMETHING IN THE SCULPTURE."),
        start(message='NOTHING HAPPENED.', result=Response.IllegalCommand))),
    Object('A VIDEO TAPE', 'TAPE', NoPlacement(),
       insert(question="TELL ME, IN ONE WORD, INTO WHAT", answer="RECORDER", removeObject='TAPE', setState=('tapeInserted', True), message='O.K. THE TAPE IS IN THE RECORDER.'), moveable=True),
    Object('A LARGE BATTERY', 'BATTERY', NoPlacement(), (
        insert(question="TELL ME, IN ONE WORD, INTO WHAT", answer="RECORDER", setState=('batteryInserted', True), removeObject='BATTERY', message='O.K.')), moveable=True),
    Object('A BLANK CREDIT CARD', 'CARD', NoPlacement(), (
        insert(question="TELL ME, IN ONE WORD, INTO WHAT", answer="SLIT", ifGE=('guardTicks', 0), removeObject='CARD', createHere='LOCK', message='POP! A SECTION OF THE WALL OPENS.....\nREVEALING SOMETHING VERY INTERESTING.'),
        insert(message="THE GUARD WON'T LET ME!", result=Response.MaybeLater)),
           moveable=True),
    Object('AN ELECTRONIC LOCK', 'LOCK', NoPlacement(),
           open(question="WHAT'S THE COMBINATION", answer="{secretCode}", removeObject=('LOCK', 'A SOLID LOOKING DOOR'), createHere='AN OPEN DOOR',
                wrong="YOU MUST HAVE THE WRONG COMBINATION OR YOU ARE NOT\nSAYING IT RIGHT.", message="THE DOOR IS SLOWLY OPENING.")),
    Object('AN ELABORATE PAPER WEIGHT', 'WEIGHT', 'CEO', (
        look(message="IT LOOKS HEAVY.")),
           moveable=True),
    Object('A LOCKED WOODEN DOOR', 'DOOR', 'ANTEROOM', (
            look(message="IT'S LOCKED.", result=Response.NotUseful),
            open(ifHas='KEY', replaceObject=('A LOCKED WOODEN DOOR', 'AN OPEN WOODEN DOOR'), message='O.K. I OPENED THE DOOR.'))),
    Object('AN OPEN WOODEN DOOR', 'DOOR', NoPlacement(), go(goTo='CEO')),
    Object('A SOLID LOOKING DOOR', 'DOOR', 'CORRIDOR', open(message="I CAN'T. IT DOESN'T WORK.", result=Response.NotUseful)),
    Object('AN OPEN DOOR', 'DOOR', NoPlacement(), go(goTo='METAL')),
    Object('AN ALERT SECURITY GUARD', 'GUARD', 'CORRIDOR'),
    Object('A SLEEPING SECURITY GUARD', 'GUARD', NoPlacement()),
    Object('A LOCKED MAINTENANCE CLOSET', 'CLOSET', 'CAFETERIA', (
            look(message="IT'S LOCKED.", result=Response.MaybeLater),
            open(ifHas='KEY', replaceObject=('A LOCKED MAINTENANCE CLOSET', 'A MAINTENANCE CLOSET'), message='O.K. THE CLOSET IS OPENED.'))),
    Object('A MAINTENANCE CLOSET', 'CLOSET', NoPlacement(), go(goTo='CLOSET')),
    Object('A PLASTIC BAG', 'BAG', 'CLOSET', (
        open(message="I CAN'T. IT'S TOO STRONG.", result=Response.NotUseful),
        look(message="IT'S A VERY STRONG BAG.", result=Response.NotUseful),
        cut(ifHas='BLADE', removeObject='BAG', createHere='TAPE', message="RIP! THE BAG GOES TO PIECES, AND SOMETHING FALLS OUT!"),
        cut(message="I CAN'T DO THAT YET.", result=Response.MaybeLater)),
           moveable=True),
    Object('AN OLDE FASHIONED KEY', 'KEY', 'ELEVATOR', moveable=True),
    Object('A SMALL METAL SQUARE ON THE WALL', 'SQUARE', 'GENERATOR', push(message="THERE'S ELECTRICITY COURSING THRU THE SQUARE!\nI'M BEING ELECTROCUTED!", result=Response.Fatal)),
    Object('A LEVER ON THE SQUARE', 'LEVER', 'GENERATOR', (
        pull(ifNotSet='glovesWorn', message="THE LEVER HAS ELECTRICITY COURSING THRU IT!\nI'M BEING ELECTROCUTED!", result=Response.Fatal),
        pull(ifNotSet='electricityOff', setState=('electricityOff', True), message="THE LEVER GOES ALL THE WAY UP AND CLICKS.\nSOMETHING SEEMS DIFFERENT NOW."))),
    Object('AN OLD MAHOGANY DESK', 'DESK', 'CEO', look(message="I CAN SEE A LOCKED DRAWER IN IT.", result=Response.NotUseful)),
    Object('A BROOM', 'BROOM', 'CLOSET', moveable=True),
    Object('A DUSTPAN', 'DUSTPAN', 'CLOSET', moveable=True),
    Object('A SPIRAL NOTEBOOK', 'NOTEBOOK', NoPlacement(), (
        look(message="THERE'S WRITING ON IT.", result=Response.NotUseful),
        read(message="IT SAYS:\n{playerName},\n  WE HAVE DISCOVERED ONE OF CHAOSES SECRET WORDS.\nIT IS: BOND-007- .TO BE USED IN A -TASTEFUL- SITUATION.")),
        moveable=True),
    Object('A MAHOGANY DRAWER', 'DRAWER', 'CEO', (
        open(ifHas='WEIGHT', message="IT'S STUCK."),
        open(message="IT's STUCK."),  # Lowercase 's' in original code
        look(message="IT LOOKS FRAGILE.", result=Response.NotUseful),
        break_(ifHas='WEIGHT', createHere=('BATTERY', 'NOTEBOOK'), makeVisible='DRAWER', message ="IT'S HARD....BUT I GOT IT. TWO THINGS FELL OUT."),
        break_(message="I CAN'T DO THAT YET.", result=Response.MaybeLater)),
        moveable=True,
        visible=False),
    Object('A GLASS CASE ON A PEDESTAL', 'CASE', 'CUBICLE', (
        look(message="I CAN SEE A GLEAMING STONE IN IT.", result=Response.NotUseful),
        cut(ifHas='BLADE', createMine='RUBY', message="I CUT THE CASE AND REACH IN TO PULL SOMETHING OUT."))),
    Object('A RAZOR BLADE', 'BLADE', 'BATHROOM', moveable=True),
    Object('A VERY LARGE RUBY', 'RUBY', NoPlacement(), moveable=True),
    Object('A SIGN ON THE SQUARE', 'SIGN', 'GENERATOR', (
        look(message="THERE'S WRITING ON IT.", result=Response.NotUseful),
        read(message="IT SAYS: WATCH OUT! DANGEROUS!")), moveable=True),
    Object('A QUARTER', 'QUARTER', NoPlacement(),
        insert(question="TELL ME, IN ONE WORD, INTO WHAT", answer="MACHINE", removeObject=('QUARTER'), createHere='CUP', message='POP! A CUP OF COFFEE COMES OUT OF THE MACHINE.'),
        moveable=True),
    Object('A COFFEE MACHINE', 'MACHINE', 'HALLWAY'),
    Object('A CUP OF STEAMING HOT COFFEE', 'CUP', NoPlacement(),
        drop(setState=('capsuleDropped', False), removeObject='CUP', message='I DROPPED THE CUP BUT IT BROKE INTO SMALL PEICES.\nTHE COFFEE SOAKED INTO THE GROUND.'),
        moveable=True),
    Object('A SMALL CAPSULE', 'CAPSULE', NoPlacement(), drop(ifHas='CUP', removeObject='CAPSULE', setState=('capsuleDropped', True), message="O.K. I DROPPED IT.\nBUT IT FELL IN THE COFFEE!"), moveable=True),
    Object('A LARGE SCULPTURE', 'SCULPTURE', 'LOBBY', (
        open(ifNotExists=('QUARTER', 'CARD'), ifSet='sculptureMessage', createHere=('CARD', 'QUARTER'), message='I OPEN THE SCULPTURE.\nSOMETHING FALLS OUT.'))),
    Object('A TALL OFFICE BUILDING', 'BUILDING', 'STREET', go(goTo='LOBBY')),
    Object('A PAIR OF SLIDING DOORS', 'DOORS', 'LOBBY', (
        go(ifSet='upButtonPushed', goTo='ELEVATOR'),
        go(message="I CAN'T GO THAT WAY AT THE MOMENT", result=Response.MaybeLater),
        look(ifSet='upButtonPushed', message="THE DOORS ARE OPEN."))),
    Object('A LARGE BUTTON ON THE WALL', 'BUTTON', 'CONTROL', (
        push(ifNotSet='wallButtonPushed', setState=('wallButtonPushed', True), message="THE BUTTON ON THE WALL GOES IN .....\nCLICK! SOMETHING SEEMS DIFFFERENT NOW."),
        push(message="NOTHING HAPPENS.", result=Response.IllegalCommand))),
    Object('A PANEL OF BUTTONS NUMBERED ONE THRU THREE', 'PANEL', 'ELEVATOR'),
    Object('A STRONG NYLON ROPE', 'ROPE', 'BASEMENT', (
        throw(ifHas='ROPE', question="TELL ME,IN ONE WORD,AT WHAT", answer="HOOK", createHere='ROPE', setState=('ropeThrown', (True, None)), wrong="O.K. I THREW IT.", message="I THREW THE ROPE AND IT SNAGGED ON THE HOOK."),
        go(ifSet='ropeThrown', goTo='PIT')), moveable=True),
    Object('A LARGE HOOK WITH A ROPE HANGING FROM IT', 'HOOK', 'PIT'),
    Object('A C.I.A. IDENTIFICATION BADGE', 'BADGE', NoPlacement(), moveable=True),
    Object('A PORTABLE TELEVISION', 'TELEVISION', 'SECURITY', (
        get(setState=('tvConnected', False)),
        connect(ifNotObjectAtLocation=('TELEVISION', 'VISITOR'), message="I DON'T SEE THE TELEVISION HERE."),
        connect(ifSet='tvConnected', message="I DID THAT ALREADY."),
        connect(ifNotAtLocation='VISITOR', message="I CAN'T DO THAT....YET!"),
        connect(setState=('tvConnected', True), message="O.K. THE T.V. IS CONNECTED.")),
        moveable=True),
    Object('A BANK OF MONITORS', 'MONITORS', 'SECURITY', (
        look(ifSet='wallButtonPushed', message="THE SCREEN IS DARK."),
        look(message="I SEE A METAL PIT 1000'S OF FEET DEEP ON ONE MONITOR.\nON THE OTHER SIDE OF THE PIT,I SEE A LARGE HOOK."))),
    Object('A CHAOS I.D. CARD', 'CARD', 'END', moveable=True),
    Object('A BANK OF MONITORS', 'MONITORS', 'MONITORING', (
        look(ifSet='wallButtonPushed', message="THE SCREEN IS DARK."),
        look(message="I SEE A ROOM WITH A CASE ON A PEDESTAL IN IT."))),
    Object('A SMALL PAINTING', 'PAINTING', 'LARGE', (
        look(message="I SEE A PICTURE OF A GRINNING JACKAL.", result=Response.NotUseful),
        get(ifNotSet='fellFromFrame', setState=('fellFromFrame', True), createHere='CAPSULE', message='SOMETHING FELL FROM THE FRAME!')),
        moveable=True),
    Object('A PAIR OF RUBBER GLOVES', 'GLOVES', 'CLOSET', (
        drop(setState=('glovesWorn', False)),
        wear(ifHas='GLOVES', setState=('glovesWorn', True), message="O.K. I'M NOW WEARING THE GLOVES.")), moveable=True),
    Object('A BOX WITH A BUTTON ON IT', 'BOX', 'LAB', moveable=True),
    # Object('ONE', 'ONE', 'ELEVATOR', push(setState=('floor', 1), setMove=('ELEVATOR', 'NORTH', 'LOBBY'), look='', message="THE DOORS CLOSE AND I FEEL AS IF THE ROOM IS MOVING.\nSUDDENLY THE DOORS OPEN AGAIN."), visible=False),
    # Object('TWO', 'TWO', 'ELEVATOR', push(setState=('floor', 2), setMove=('ELEVATOR', 'NORTH', 'HALLWAY'), look='', message="THE DOORS CLOSE AND I FEEL AS IF THE ROOM IS MOVING.\nSUDDENLY THE DOORS OPEN AGAIN."), visible=False),
    # Object('THREE', 'THREE', 'ELEVATOR', push(setState=('floor', 1), setMove=('ELEVATOR', 'NORTH', 'CORRIDOR'), look='', message="THE DOORS CLOSE AND I FEEL AS IF THE ROOM IS MOVING.\nSUDDENLY THE DOORS OPEN AGAIN."), visible=False),
    Object('SLIT', 'SLI', 'CORRIDOR', visible=False),

    # These are not in the original game's object list but are included here
    # so that every target is a direction or an object.
    # In the game, "BUT" is a special cased string when used for these purposes.
    Object('AN UP BUTTON', 'BUTTON', 'LOBBY', (
        push(ifNotSet='upButtonPushed', setState=('upButtonPushed', True), message='THE DOORS OPEN WITH A WHOOSH!', result=Response.NewlySeen),
        push(message="I DON'T SEE THAT HERE")), visible=False),   # This should be considered successful
    Object('A BUTTON ON A BOX', 'BUTTON', 'LAB', (
        push(ifNotHas='BOX', message="I DON'T SEE THAT HERE."),
        push(ifHas='BOX', ifAtLocation=('CUBICLE', 'CONTROL'), setState=('floor', 1), setMove=('ELEVATOR', 'NORTH', 'LOBBY'), goTo='STREET', message="I PUSH THE BUTTON ON THE BOX AND\nTHERE IS A BLINDING FLASH....\n"),
        push(message="I PUSH THE BUTTON ON THE BOX AND\nNOTHING HAPPENS.", result=Response.IllegalCommand),),
        visible=False),
)