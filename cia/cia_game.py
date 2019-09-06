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
import random

class CIA(Game):
    def __init__(self):
        state = State()
        world = World(objects, verbs, locations)
        prompts = ('WHAT DO YOU THINK WE SHOULD DO? ', 'ENTER YOUR NAME PARTNER? ')
        Game.__init__(self, world, state, prompts)
        state.location = world.locations['ON A BUSY STREET']
        self.state['playerName'] = None
        self.state['secretCode'] = str(9 * random.choice(range(9)))[1:]
        self.state['upButtonPushed'] = False
        self.state['floor'] = 1
        self.state['ropeThrown'] = False
        self.state['glovesWorn'] = False
        self.state['fellFromFrame'] = False
        self.state['capsuleDropped'] = False
        self.state['boxButtonPushed'] = False
        self.state['batteryInserted'] = False
        self.state['tvConnected'] = False
        self.state['guardAwakened'] = False
        self.state['sleepTimer'] = -1
        self.state['tapeInserted'] = False
        self.state['sculptureMessage'] = False
        self.state['electricityOff'] = False
        self.state['combination'] = 12345
        self.state['guardTicks'] = -1

        self.state.inventory.Add(world.objects['BADGE'])

    def Run(self, commands):
#        self.world.print()
        Game.Run(self, commands)

    def Start(self):
        print("        C.I.A  ADVENTURE")
        self.Do("LOOK", echo=False)
        self.state['playerName'], expected = self.Input("ENTER YOUR NAME PARTNER? ")
        self.Output("WRITING ON THE WALL SAYS\nIF YOU WANT INSTRUCTIONS TYPE:ORDERS PLEASE")
        return

    def Tick(self):
        k = str(self.state.inventory)
        m = ""
        if self.state['guardTicks'] != -1:
            self.state['guardTicks'] -= 1
            if self.state['guardTicks'] == 0:
                self.ReplaceObject(self.world.objects['A SLEEPING SECURITY GUARD'], self.world, objects['AN ALERT SECURITY GUARD'])
                self.state['guardTicks'] = -1
                self.state['guardAwakened'] = True
                m = "I HEAR A NOISE LIKE SOMEONE IS YAWNING."
        return m

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

cia = CIA()
#commands = sequence
commands = open(r"..\basic\CIANEW.ADL", "r")
cia.Run(commands)
