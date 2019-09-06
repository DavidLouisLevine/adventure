# This is a game engine that was created to emulate the "C.I.A. Adventure" game written by Hugh Lampert circa 1982
# The game content is is a separate folder
# The engine could implement many other games

from adventure.target import Target
from adventure.direction import Direction
from adventure.placement import NoPlacement
from adventure.response import Response
from adventure.util import StartsWith
import numpy as np

class Game:
    def __init__(self, world, state, prompt):
        self.world = world
        self.state = state
        self.prompt = prompt
        self.quitting = False
        self.inputFile = open(r"..\basic\CIANEW.ADL", "r")
        self.scriptOutputFile = open(r"c:\users\david\onedrive\documents\programming\cia\ciascript.adv", "w")
        self.nextLine = None

    def NextLine(self):
        if self.nextLine is not None:
            l = self.nextLine
            self.nextLine = None
            return l

        while True:
            l = self.inputFile.readline()
            if l == "":
                self.inputFile.close()
                self.inputFile = None
                break
            if l[0] != '#':
                break

        return l

    def ReadToPrompt(self):
        expected = ""
        while True:
            t = self.NextLine()
            if t == "":
                break
            if StartsWith(t, self.prompt):
                self.nextLine = t
                break
            expected += t
        return expected

    def Input(self, prompt):
        expected = None
        if self.inputFile is not None:
            print(prompt + '? ', end='')
            commandLine = self.NextLine()
            assert StartsWith(commandLine, self.prompt)
            command = commandLine[len(self.prompt):]
            expected = self.ReadToPrompt()
            if command != "":
                print(command, end='')

            # expected = ""
            # while True:
            #     t = self.inputFile.readline()
            #     if t == "":
            #         break
            #
            #     if t[:4] == '---@':
            #         break
            #
            #     if t[0] != '#':
            #         expected += t
            #
            # if t == "":
            #     self.inputFile.close()
            #     self.inputFile = None
            #
            # if u != "":
            #     print(u, end='')

        if self.inputFile is None:
            command = input(prompt)
            expected = None

        if self.scriptOutputFile is not None:
            self.scriptOutputFile.write(command)

        return command, expected

    def DoAction(self, action):
        try:
            i = action.index(' ')
            verbStr = action[:i]
        except:
            i = -1
            verbStr = action

        verb = self.world.verbs[verbStr]
        if verb is None:
            return "I DON'T KNOW HOW TO DO THAT."

        target = None
        original_value = None
        if i != -1:
            targetStr = action[i + 1:]

            value = Direction.FromName(targetStr)
            locationSatisfied = not verb.targetInRoom and not verb.targetInventory
            if value is None:
                value = self.world.objects.Find(targetStr)
                original_value = value
                if value is not None and self.state.inventory.Has(value):
                    #self.value = value
                    if verb.targetInventory:
                        locationSatisfied = True
                else:
                    value = self.world.objects.Find(targetStr, self.state.location)
                    if verb.targetInRoom:
                        locationSatisfied = True

                if value is not None and not locationSatisfied:
                    value = None

            target = Target(value)

        if (target is None or target.value is None) and not (verb.targetOptional or verb.targetNever):
            return "I DON'T KNOW WHAT IT IS YOU ARE TALKING ABOUT."

        currentLocation = self.state.location
        m = verb.Do(target, self)

        # If the location changed, execute the new location's response
        if self.state.location != currentLocation:
            m += self.Look()
            if self.state.location.responses is not None:
                currentLocation = self.state.location
                r = Response.Respond(self.state.location.responses, self.world.verbs['GO'], self)
                if r is not None:
                    if m is not "":
                        m += '\n'
                    m += r
                    if self.state.location != currentLocation:
                        m += '\n' + self.Look()
        return m


    def Do(self, action, echo=True):
        if echo:
            print("> ", action)

        if action[-1] == '\n':
            action = action[:-1]

        m = self.DoAction(action)
        if not m is None and not m == "":
            print(m)
            return m

    def Run(self, actions):
        self.ReadToPrompt()

        t = 0
        prompt = self.prompt
        while not self.quitting:
            if t < len(actions):
                str = actions[t]
                print(prompt + str)
            else:
                str, expectedMessage = self.Input(prompt)

            temp = self.Do(str, echo=False)
            if temp is not None:
                actualMessage = temp + "\n\n"
                if expectedMessage is not None and expectedMessage != actualMessage and expectedMessage != "":
                    print("ERROR: Expected Message:\n", expectedMessage, sep='')
                    print("---------")
                    print("ERROR: Actual Message:\n", actualMessage)
                    print("---------")
                    n = min(len(actualMessage), len(expectedMessage))
                    k = np.array(list(expectedMessage[:n])) == np.array(list(actualMessage[:n]))
                    j = np.argwhere(k == False)[0][0]
                    o = 9
            else:
                if expectedMessage is not None and expectedMessage != "":
                    print("ERROR: Actual message is empty but expected message is:", expectedMessage)

            print(self.Tick())
            t += 1

        if self.state.isDead:
            print("I'M DEAD!\nYOU DIDN'T WIN")

    def Tick(self, target, game):
        pass

    def Look(self, at=None):
        return self.world.verbs['LOOK'].Do(at, self)

    def GoTo(self, location):
        self.state.location = self.world.ResolveLocation(location)

    def CreateHere(self, object):
        self.world.MoveObject(object, self.state.location)

    def ReplaceObject(self, old, new):
        self.world.RemoveObject(old)
        self.CreateHere(new)

    def Has(self, object):
        object = self.world.ResolveObject(object)
        return self.state.inventory.Has(object)

    def Exists(self, object):
        return object.placement != NoPlacement

    def __str__(self):
        return str(self.state.location) + str(self.state.inventory)