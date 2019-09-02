# This is a port of the game "C.I.A. Adventure" downloaded from https://www.myabandonware.com/game/cia-adventure-1ya on 2019-08-25
# The description on that site reads:
#   C.I.A. Adventure is a video game published in 1982 on DOS by International PC Owners.
#   It's an adventure game, set in an interactive fiction, spy / espionage and contemporary themes,
#   and was also released on Commodore 64.

# The site at http://gamingafter40.blogspot.com/2013/07/adventure-of-week-cia-adventure-1980.html, downloaded 2019-08-31
# credits the game to Hugh Lampert. That site also has a complete walk through.

from adventure.game import Game
from adventure.world import World
from adventure.state import State
from cia.cia_verb import verbs
from cia.cia_object import objects
from cia.cia_location import locations

class CIA(Game):
    def __init__(self):
        world = World(objects, verbs, locations)
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
