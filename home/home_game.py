# This is a simple four-room adventure, originally from MIT's 6.86x Machine Learning course

from adventure.game import Game
from adventure.world import World
from adventure.state import State
from adventure.response import Response
from home.home_verb import verbs
from home.home_object import objects
from home.home_location import locations
import random

class Home(Game):
    def __init__(self):
        Game.__init__(self)
        self.quests = (('watch', 'tv'), ('exercise', 'bike'), ('eat', 'apple'), ('sleep', 'bed'))
        self.questNames = ('You are bored.', 'You are getting fat.', 'You are hungry.','You are sleepy.')

    def Init(self):
        state = State()
        world = World(objects, verbs, locations)
        prompts = ('WHAT DO YOU THINK WE SHOULD DO? ', 'ENTER YOUR NAME PARTNER? ', 'TELL ME,IN ONE WORD,AT WHAT? ')
        outputFile = None
        Game.Init(self, world, state, prompts, outputFile=outputFile)

    def NewGame(self):
        Game.NewGame(self)
        n = random.choice(range(len(self.quests)))
        q = self.quests[n]
        self.questCommand = self.world.verbs[q[0]].i, self.world.objects[q[1]].i
        self.questName = self.questNames[n]
        self.prompt = self.questName + ":"

        self.state['quest'] = self.world.verbs[self.questCommand[0]].abbreviation + ' ' + self.world.objects[self.questCommand[1]].abbreviation

        self.defaultReward = -0.01
        self.rewards = {
            Response.Success: self.defaultReward,
            Response.QuestCompleted: 1,
            Response.IllegalCommand: -0.1 + self.defaultReward,
            Response.NewlySeen: 0,
        }

        self.state.location = self.world.locations[random.choice(range(len(self.world.locations)))]

        return self.state.location.Name(), self.questName, False

    def Run(self, commands):
#        self.world.print()
        Game.Run(self, commands)

    def Start(self):
        self.Output("        Welcome Home!")
        self.Output(self.Look()[0])
        return

if __name__ == '__main__':
    sequence = (
        "GO NORTH",
        "eat apple",)

    home = Home()
    home.Init()
    home.NewGame()

    #commands = sequence
    commands = None

    home.Run(commands)
