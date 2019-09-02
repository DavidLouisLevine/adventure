from adventure.target import Target
from adventure.direction import Direction
import numpy as np

class Game:
    def __init__(self, world, state):
        self.world = world
        self.state = state
        self.quitting = False
        self.inputFile = open("ciatest.adv", "r")
        self.scriptOutputFile = open(r"c:\users\david\onedrive\documents\programming\cia\ciascript.adv", "w")
        self.inResponse = False

    def Input(self, prompt):
        expected = None
        if self.inputFile is not None:
            print(prompt + '? ', end='')
            u = ""
            while u == "":
                t = self.inputFile.readline()
                if t == "":
                    break
                if t[0] != '#':
                    u = t

            expected = ""
            while True:
                t = self.inputFile.readline()
                if t == "":
                    break

                if t[:4] == '---@':
                    break

                if t[0] != '#':
                    expected += t

            if t == "":
                self.inputFile.close()
                self.inputFile = None

            if u != "":
                print(u, end='')

        if self.inputFile is None:
            u = input(prompt)
            t = None

        if self.scriptOutputFile is not None:
            self.scriptOutputFile.write(u)

        return (u, expected)

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
        if i != -1:
            targetStr = action[i + 1:]

            value = Direction.FromName(targetStr)
            locationSatisfied = not verb.targetInRoom and not verb.targetInventory
            if value is None:
                value = self.world.objects.Find(targetStr)
                if value is not None and self.state.inventory.Has(value):
                    self.value = value
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
        if self.state.location != currentLocation:
            m += self.Look()
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
        t = 0
        prompt = "\nWHAT DO YOU THINK WE SHOULD DO? "
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
                    print("ERROR: Expected Message:\n", expectedMessage)
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

            self.Tick()
            t += 1

        if self.state.isDead:
            print("I'M DEAD!\nYOU DIDN'T WIN")

    def Tick(self, target, game):
        pass

    def Look(self):
        return self.world.verbs['LOOK'].Do(None, self)

    def TravelTo(self, location):
        self.state.location = self.world.ResolveLocation(location)

    def CreateHere(self, object):
        self.world.MoveObject(object, self.state.location)

    def Has(self, object):
        object = self.world.ResolveObject(object)
        return self.state.inventory.Has(object)

    def __str__(self):
        return str(self.state.location) + str(self.state.inventory)