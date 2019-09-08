from adventure.location import Location
from cia.cia_verb import go
from adventure.direction import Direction
import random

def GoBuilding(game, *args, **kwargs):
    if game.state.location==game.world.locations['ON A BUSY STREET']:
        game.GoTo('LOBBY')
        if not game.Has('BADGE'):
            game.GoTo('LOBBY')
            return ""
        else:
            m = game.Look()
            m += '\nTHE DOOR MAN LOOKS AT MY BADGE AND THEN THROWS ME OUT.\n'
            game.GoTo('STREET')
            m += game.Look()
            return m

locations = (
    Location('STREET', 'ON A BUSY STREET', (0, 0, 0, 0),
        go(ifHas='RUBY', isWin=True, message="HURRAY! YOU'VE RECOVERED THE RUBY!\nYOU WIN!")),
    Location('VISITOR', 'IN A VISITOR\'S ROOM', (0,  0,  'LOBBY',  0)),
    Location('LOBBY', 'IN THE LOBBY OF THE BUILDING', ('STREET', 0, 'ANTEROOM', 'VISITOR'),
         go(ifHas='BADGE', goTo='STREET', message="THE DOOR MAN LOOKS AT MY BADGE AND THEN THROWS ME OUT.")),
    Location('ANTEROOM', 'IN A DINGY ANTE ROOM', (0, 0, 0, 'LOBBY')),
    Location('CEO', 'IN THE COMPANY PRESIDENT\'S OFFICE', (0, 0, 0, 'ANTEROOM')),
    Location('CUBICLE', 'IN A SMALL SOUND PROOFED CUBICLE', (0, 'PLAIN', 0, 0), (
        go(ifNotSet='boxButtonPushed', isFatal=True, message="SIRENS GO OFF ALL AROUND ME!\nGUARDS RUN IN AND SHOOT ME TO DEATH!"),
        go(condition=lambda g:g.world.locations['CUBICLE'].moves[Direction.EAST] != 0, setMove=(('CUBICLE', Direction.EAST, 0)), message="A SECRET DOOR SLAMS DOWN BEHIND ME!"))),
    Location('SECURITY', 'IN A SECURITY OFFICE', (0, 0, 'HALLWAY', 0)),
    Location('HALLWAY', 'IN A SMALL HALLWAY', (0, 'CAFETERIA', 'ELEVATOR', 'SECURITY')),
    Location('ELEVATOR', 'IN A SMALL ROOM', ('LOBBY', 0, 0, 0)),
    Location('CORRIDOR', 'IN A SHORT CORRIDOR', (0, 'SIDE', 0, 'ELEVATOR'), (
        go(ifNotHas='CARD', goTo='ELEVATOR', message="THE GUARD LOOKS AT ME SUSPICIOUSLY, THEN THROWS ME BACK."),
        go(ifHas='COFFEE', isSet='capsuleDropped', replaceObject=('AN ALERT SECURITY GUARD', 'A SLEEPING SECURITY GUARD'),
           setState=(('capsuleDropped', False), ('guardTicks', 5 + int(10*random.choice(range(10))))),
           message="THE GUARD TAKES MY COFFEE\nAND FALLS TO SLEEP RIGHT AWAY."),
        go(ifSet='guardAwakened', isFatal=True, message="THE GUARD DRAWS HIS GUN AND SHOOTS ME!"))),
    Location('METAL', 'IN A HALLWAY MADE OF METAL', (0, 0, 'PLAIN', 'CORRIDOR'), go(ifNotSet='electricityOff', isFatal=True, message="THE FLOOR IS WIRED WITH ELECDRICITY!\nI'M BEING ELECTROCUTED!")),
    Location('PLAIN', 'IN A SMALL PLAIN ROOM', ('CUBICLE', 0, 0, 'METAL')),
    Location('CLOSET', 'IN A MAINTENANCE CLOSET', (0, 0, 'CAFETERIA', 0)),
    Location('CAFETERIA', 'IN A CAFETERIA', ('HALLWAY', 0, 0, 0)),
    Location('SIDE', 'IN A SIDE CORRIDOR', ('CORRIDOR', 0, 'GENERATOR', 0)),
    Location('GENERATOR', 'IN A POWER GENERATOR ROOM', (0, 0, 0, 'SIDE')),
    Location('BASEMENT', 'IN A SUB-BASEMENT BELOW THE CHUTE', (0, 0, 'COMPLEX', 0)),
    Location('COMPLEX', 'IN THE ENTRANCE TO THE SECRET COMPLEX', (0, 'LEDGE', 'MONITORING', 'BASEMENT')),
    Location    ('MONITORING', 'IN A SECRET MONITORING ROOM', (0, 0, 0, 'COMPLEX')),
    Location('LEDGE', 'ON A LEDGE IN FRONT OF A METAL PIT 1000\'S OF FEET DEEP', ('COMPLEX', 0, 0, 0)),
    Location('PIT', 'ON THE OTHER SIDE OF THE PIT', ( 0, 0, 'LONG', 0)),
    Location('LONG', 'IN A LONG CORRIDOR', (0, 'NARROW', 'LARGE', 'PIT')),
    Location('LARGE', 'IN A LARGE ROOM', (0, 'EXAM', 0, 'LONG')),
    Location('LAB', 'IN A SECRET LABORATORY', (0, 0, 'NARROW', 0)),
    Location('NARROW', 'IN A NARROW CROSS CORRIDOR', ('LONG', 0, 0, 'LAB')),
    Location('EXAM', 'IN A CROSS EXAMINATION ROOM', ('LARGE', 'CHIEF', 0, 0)),
    Location('BATHROOM', 'IN A SMALL BATHROOM', (0, 0, 'CHIEF', 0)),
    Location('CHIEF', 'IN THE OFFICE OF THE CHIEF OF CHAOS', ('EXAM', 'END', 0, 'BATHROOM')),
    Location('CONTROL', 'IN THE CHAOS CONTROL ROOM', (0, 0, 'END', 0)),
    Location('END', 'NEAR THE END OF THE COMPLEX', ('CHIEF', 0, 0, 'CONTROL'))
)
