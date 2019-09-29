# This is a port of Hugh Lampert's "C.I.A. Adventure" game, downloaded from https://www.myabandonware.com/game/cia-adventure-1ya on 2019-08-25
# The description on that site reads:
#   C.I.A. Adventure is a video game published in 1982 on DOS by International PC Owners.
#   It's an adventure game, set in an interactive fiction, spy / espionage and contemporary themes,
#   and was also released on Commodore 64.

# The site at http://gamingafter40.blogspot.com/2013/07/adventure-of-week-cia-adventure-1980.html,
# downloaded 2019-08-31 has a complete walk through. With a great deal of perseverance, it's possible to
# play the entire game without looking at the source code. The most important hint is that if
# you're ever given a sequence of numbers to enter, make sure you keep the original spacing.

from adventure.game import Game
from adventure.world import World
from adventure.state import State
from adventure.response import Response
from cia.cia_verb import verbs
from cia.cia_object import objects
from cia.cia_location import locations
import random

class CIA(Game):
    def __init__(self):
        super().__init__()
        self.questNames = ()

    def Init(self):
        state = State()
        world = World(objects, verbs, locations)
        prompts = ('WHAT DO YOU THINK WE SHOULD DO? ', 'ENTER YOUR NAME PARTNER? ', 'TELL ME,IN ONE WORD,AT WHAT? ', 'TELL ME, IN ONE WORD, INTO WHAT? ', 'WHAT\'S THE COMBINATION? ')
        super().Init(world, state, prompts)

    def NewGame(self):
        Game.NewGame(self)
        self.questName = "Get Elevator"
        self.quest = self.world.verbs['GO'], self.world.objects['BUILDING']

        self.state.location = self.world.locations['ON A BUSY STREET']

        self.state['playerName'] = None
        code = ""
        for _ in range(5):
            code += str(random.choice(range(9)))
        self.state['secretCode'] = '1 2 3 4 5' # code
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
        self.state['tapeInserted'] = False
        self.state['wallButtonPushed'] = False
        self.state['sculptureMessage'] = False
        self.state['electricityOff'] = False
        self.state['combination'] = 12345
        self.state['guardTicks'] = -1

        self.defaultReward = -0.01
        self.rewards = {
            Response.Success: self.defaultReward,
            Response.QuestCompleted: 1,
            Response.IllegalCommand: -0.1 + self.defaultReward,
            Response.Fatal: -1,
            Response.MaybeLater: 0.04 + self.defaultReward,
            Response.NotUseful: -0.02 + self.defaultReward,
            Response.NewlySeen: 0.06 + self.defaultReward,
            Response.MightBeUseful: 0.02 + self.defaultReward,
        }

        self.state.inventory.Add(self.world.objects['BADGE'])
        return self.state.location.Name(), self.quest, False

    def Run(self, commands, steps=None):
#        self.world.print()
        Game.Run(self, commands, steps=steps)

    def Start(self):
        self.Output("        C.I.A  ADVENTURE")
        self.Do("LOOK")
        self.state['playerName'], expected = self.Input("ENTER YOUR NAME PARTNER? ")
        self.Output("WRITING ON THE WALL SAYS\nIF YOU WANT INSTRUCTIONS TYPE:ORDERS PLEASE")
        return

    def PreTick(self):
        assert len(self.state.inventory.GetStrings(self.world)) == self.state.inventory.size
        k = str(self.state.inventory)
        m = ""
        result = Response.Success
        if self.Has('RUBY') and self.state.location == self.world.locations['STREET']:
            result = Response.QuestCompleted
            m = "HURRAY! YOU'VE RECOVERED THE RUBY!\nYOU WIN!"

        return m, result

    def PostTick(self):
        m = ""
        result = Response.Success
        if self.state['guardTicks'] != -1:
            self.state['guardTicks'] -= 1
            if self.state['guardTicks'] == 0:
                self.ReplaceObject(self.world.objects['A SLEEPING SECURITY GUARD'], self.world.objects['AN ALERT SECURITY GUARD'])
                self.state['guardTicks'] = -1
                self.state['guardAwakened'] = True
                m = "I HEAR A NOISE LIKE SOMEONE IS YAWNING."
        # This can happen after we enter the CORRIDOR because we can drop the CAPSULE when in the CORRIDOR
        if self.Has('CUP') and self.state['capsuleDropped'] == True and self.AtLocation('CORRIDOR'):
            self.ReplaceObject('AN ALERT SECURITY GUARD', 'A SLEEPING SECURITY GUARD')
            self.state['capsuleDropped'] = False
            self.state['guardTicks'] = 10 #5 + int(10*random.choice(range(10)))
            m = "THE GUARD TAKES MY COFFEE\nAND FALLS TO SLEEP RIGHT AWAY."
        return m, result

    def PreCommand(self, verb, target):
        assert verb is not None
        #assert target is not None
        assert self.state.location is not None
        if verb.Is('OPEN') and target is not None and target.IsObject() and target.value.Is('A LOCKED WOODEN DOOR') \
                and self.state.location.Is('ANTEROOM') \
                and self.Has('KEY'):
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!OPENED WOODEN DOOR!!!!!!!!!!!!!!!!!!!!!!!")
            jj = 99

if __name__ == '__main__':
    sequence = (
        "GO BUILDING",
        "INVENTORY",
        "WEAR BADGE",
        "DROP BADGE",
        "INVENTORY",
        "LOOK",
        "GO BUILDING",
        "GO WEST")

    cia = CIA()
    cia.Init()
    cia.NewGame()
    cia.printWhenStreaming = False
    cia.Trim(open(r"..\basic\CIA_WALK.ADL", "r"), steps=25)
    cia.NewGame()

    #commands = sequence

    # This is a complete walkthrough of the adventure, along with all output from the original game
    #commands = open(r"..\basic\CIA_WALK.ADL", "r")
    commands = None

    cia.Run(commands)
