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
from home.home_verb import verbs
from home.home_object import objects
from home.home_location import locations
import random

class Home(Game):
    def __init__(self):
        Game.__init__(self)

    def Init(self):
        state = State()
        world = World(objects, verbs, locations)
        prompts = ('WHAT DO YOU THINK WE SHOULD DO? ', 'ENTER YOUR NAME PARTNER? ', 'TELL ME,IN ONE WORD,AT WHAT? ')
        Game.Init(self, world, state, prompts)

    def NewGame(self):
        Game.NewGame(self)
        q = random.choice((('eat', 'apple'), ('exercise', 'bike'), ('sleep', 'bed'), ('watch', 'tv')))
        self.quest = self.world.verbs[q[0]].i, self.world.objects[q[1]].i

        self.state.location = self.world.locations['Bedroom']

        return self.state.location.Name(), self.quest, False

    def Run(self, commands):
#        self.world.print()
        Game.Run(self, commands)

    def Start(self):
        self.Output("        Welcome Home!")
        self.Do("LOOK")
        return

    def Tick(self):
        pass

if __name__ == '__main__':
    sequence = (
        "GO NORTH",
        "eat apple",)

    home = Home()
    home.Init()
    home.NewGame(('sleep',  'bed'))

    #commands = sequence
    #commands = open(r"..\basic\CIANEW.ADL", "r")
    commands = None
    # commands can be None, a sequence of text commands, or a file containing text commands
    home.Run(commands)
