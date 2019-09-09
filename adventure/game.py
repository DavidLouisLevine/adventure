# This is a game engine that was created to emulate the "C.I.A. Adventure" game written by Hugh Lampert circa 1982
# The game content is is a separate folder
# The engine could implement many other games

from adventure.target import Target
from adventure.direction import Direction
from adventure.placement import NoPlacement, InventoryPlacement, LocationPlacement
from adventure.response import Response
from adventure.util import StartsWith

class Game:
    def Init(self, world, state, prompts):
        self.world = world
        self.state = state
        self.prompt = prompts[0]
        self.prompts = prompts
        self.quitting = False
        self.inputFile = None
        self.printWhenStreaming = False # If False, only print errors when commands are being read from the input file
        self.scriptOutputFile = open(r"c:\users\david\onedrive\documents\programming\cia\ciascript.adv", "w")
        self.nextLine = None

    def NewGame(self, quest):
        self.state.Init()
        self.quest = quest

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
        if self.inputFile is None:
            return ""

        expected = ""
        while True:
            t = self.NextLine()
            if t == "":
                break
            if StartsWith(t, self.prompts) is not None:
                self.nextLine = t
                break
            expected += t
        return expected

    def Input(self, prompt, readExpected=True):
        expected = None
        if self.inputFile is not None:
            self.Output(prompt + '? ', end='')
            commandLine = self.NextLine()
            start = StartsWith(commandLine, self.prompts)
            assert start is not None
            command = commandLine[start:]
            if readExpected:
                expected = self.ReadToPrompt()
            if command != "":
                self.Output(command, end='')

        if self.inputFile is None:
            command = input(prompt)
            expected = None

        if self.scriptOutputFile is not None:
            self.scriptOutputFile.write(command)

        if command != "" and command[-1] == '\n':
            command = command[:-1]
        return command, expected

    def Output(self, *args, **kwargs):
        if self.inputFile is None or self.printWhenStreaming:
            return print(*args, **kwargs)

    def DoTarget(self, verb, target):
        if verb is None:
            return "I DON'T KNOW HOW TO DO THAT."

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

    def DoAction(self, action):
        if ' ' in action:
            i = action.index(' ')
            verbStr = action[:i]
        else:
            i = -1
            verbStr = action
        verb = self.world.verbs[verbStr]
        target = None
        if verb is not None:
            original_value = None
            if i != -1:
                targetStr = action[i + 1:]

                value = Direction.FromName(targetStr)
                if value is None:
                    value = self.world.objects.Find(targetStr, self.state.location)
                    if value is None:
                        value = self.world.objects[targetStr]

                target = None if value is None else Target(value)
        return self.DoTarget(verb, target)

    def Do(self, action):
        if action[-1] == '\n':
            action = action[:-1]

        m = self.DoAction(action)
        if not m is None and not m == "":
            self.Output(m)
            return m

    # commands can be either a file with read access or a list of commands
    def Run(self, commands):
        if type(commands) == tuple:
            actions = commands
        else:
            self.inputFile = commands
            actions = ()

        self.ReadToPrompt()

        t = 0
        self.Start()
        prompt = self.prompt
        while not self.quitting:
            if t < len(actions):
                s = actions[t]
                self.Output(prompt + s)
            else:
                s, expectedMessage = self.Input(prompt)

            if s != "":
                message = self.Do(s)
                if expectedMessage=="":
                    expectedMessage = self.ReadToPrompt() # Occurs when a question is prompted after the command

                self.ValidateOutput(expectedMessage, message)

            self.Output(self.Tick())
            t += 1

        if self.state.isDead:
            self.Output("I'M DEAD!\nYOU DIDN'T WIN")

    def Start(self, game):
        pass

    def Tick(self, target, game):
        pass

    def Look(self, at=None):
        return self.world.verbs['LOOK'].Do(at, self)

    def GoTo(self, location):
        self.state.location = self.world.ResolveLocation(location)

    def CreateHere(self, object):
        object = self.world.ResolveObject(object)
        self.MoveObject(object, self.state.location)

    def ReplaceObject(self, old, new):
        self.RemoveObject(old)
        self.CreateHere(new)

    def Has(self, object):
        object = self.world.ResolveObject(object)
        return self.state.inventory.Has(object)

    def Exists(self, object):
        object = self.world.ResolveObject(object)
        return type(object.placement) != NoPlacement

    def IsHere(self, object):
        object = self.world.ResolveObject(object)
        return type(object.placement) == InventoryPlacement or\
               (type(object.placement) == LocationPlacement and object.placement.location == self.state.location)

    def AtLocation(self, location):
        return self.state.location == self.world.ResolveLocation(location)

    def RemoveObject(self, object):
        object = self.world.ResolveObject(object)
        self.state.inventory.Remove(object)
        original_object = object
        if object is None:
            object = self.world.ResolveObject(original_object) # for debug
        object.placement = NoPlacement()

    def MoveObject(self, object, location):
        self.state.inventory.Remove(object)
        original_object = object
        object = self.world.ResolveObject(object)
        if object is None:
            object = self.world.ResolveObject(original_object)
        location = self.world.ResolveLocation(location)
        object.placement = LocationPlacement(location)

    def __str__(self):
        return str(self.state.location) + self.state.inventory.string(self.world)

    def ValidateOutput(self, expectedMessage, actualMessage):
        if actualMessage is not None:
            actualMessage = actualMessage + "\n\n"
            if expectedMessage is not None and expectedMessage != actualMessage and expectedMessage != "":
                print("ERROR: Expected Message:\n", expectedMessage, sep='')
                print("---------")
                print("ERROR: Actual Message:\n", actualMessage)
                print("---------")
                n = min(len(actualMessage), len(expectedMessage))
                i = 0
                for i in range(n):
                    if expectedMessage[i] != actualMessage[i]:
                        break;
                    i += 1
                return False
        else:
            if expectedMessage is not None and expectedMessage != "":
                print("ERROR: Actual message is empty but expected message is:", expectedMessage)
                return False
        return True
