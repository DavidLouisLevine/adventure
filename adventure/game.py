# This is a game engine that was created to emulate the "C.I.A. Adventure" game written by Hugh Lampert circa 1982
# The game content is in separate folders
# The engine is designed to implement many different adventure games

from adventure.target import Target
from adventure.direction import Direction
from adventure.placement import NoPlacement, InventoryPlacement, LocationPlacement
from adventure.response import Response
from adventure.util import StartsWith, MakeTuple
from adventure.verb import BuiltInVerbs
from copy import copy, deepcopy

class Game:
    def Init(self, world, state, prompts, outputFile=None):
        self.startingWorld = world
        self.world = deepcopy(self.startingWorld)
        self.startingState = state
        self.state = deepcopy(self.startingState)
        self.prompt = prompts[0]
        self.prompts = prompts
        self.quitting = False
        self.inputFile = None
        self.printWhenStreaming = True # If False, only print errors when commands are being read from the input file
        self.scriptOutputFile = outputFile
        self.nextLine = None
        self.questCommand = None
        self.rewards = {}

    def NewGame(self):
        self.state.Init()
        self.world = deepcopy(self.startingWorld)
        self.state = deepcopy(self.startingState)
        self.nextLine = None
        self.quitting = False
        self.inputFile = None
        for object in self.world.objects:
            object.seen = False
        for location in self.world.locations:
            location.seen = False

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
        # if verb is not None and verb.name == 'PUSH' and target is not None and target.IsObject() and target.value.i == self.world.objects['AN UP BUTTON'].i and \
        #     self.state.location.abbreviation == 'LOBBY':
        #     print("PUSH UP BUTTON!!!!!!!!!!!!")

        # if verb is not None and verb.name == 'GET' and target is not None and target.IsObject() and target.value.i == self.world.objects['KEY'].i and \
        #     self.state.location.abbreviation == 'ELEVATOR':
        #     print("GET KEY!!!!!!!!!!!!")

        self.PreCommand(verb, target)

        if verb is None:
            return "I DON'T KNOW HOW TO DO THAT.", 0, Response.IllegalCommand

        if target is not None and target.value is not None and verb.targetNever:
            return "I DON'T KNOW WHAT IT IS YOU ARE TALKING ABOUT.", 0, Response.IllegalCommand

        if (target is None or target.value is None) and not (verb.targetOptional or verb.targetNever):
            return "I DON'T KNOW WHAT IT IS YOU ARE TALKING ABOUT.", 0, Response.IllegalCommand

        if target is not None and target.IsDirection() and verb != self.BaseVerb('GO'):
            return "I DON'T KNOW WHAT IT IS YOU ARE TALKING ABOUT.", 0, Response.IllegalCommand

        currentLocation = self.state.location
        m, reward, result = verb.Do(target, self)

        # If the location changed, execute the new location's response
        if self.state.location != currentLocation:
            m += self.Look()[0]
            if self.state.location.responses is not None:
                currentLocation = self.state.location
                m2, reward2, result = Response.Respond(self.state.location.responses, self.world.verbs['GO'], self)
                if m2 is not None and m2 != "":
                    if m is not "":
                        m += '\n'
                    m += m2
                    reward += reward2
                    if self.state.location != currentLocation:
                        m += '\n' + self.Look()[0]
            if m is None or m == "":
                m = self.Look()

        reward += self.UpdateSeen(verb)
        return m, reward, result

    def UpdateSeen(self, verb):
        reward = 0
        if not self.state.location.seen:
            reward += self.rewards[Response.NewlySeen]
            self.state.location.    seen = True

        for object in self.world.objects:
            if not object.seen and (object.placement.location == self.state.location or object.placement == InventoryPlacement):
                reward += self.rewards[Response.NewlySeen]
                object.seen = True

        if verb is not None:
            verb.seen = True

        return reward

    def DoAction(self, action):
        if action == "GO BUILDING":
            jj = 9
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
                while action[i] == ' ':
                    i += 1
                targetStr = action[i:]

                value = Direction.FromName(targetStr)
                if value is None:
                    value = self.world.objects.Find(targetStr, self.state.location)
                    if value is None:
                        value = self.world.objects[targetStr]

                target = None if value is None else Target(value)
        m, reward, result = self.DoTarget(verb, target)
        return m, result, (verb, target)

    def Do(self, action):
        if action[-1] == '\n':
            action = action[:-1]

        m, result, action = self.DoAction(action)
        if not m is None and not m == "":
            self.Output(m)
            return m, result, action

        return "", Response.IllegalCommand, None

    # Command input can come from a sequence of strings, from a file open for reading, or entirely from the user
    def Run(self, commands, steps=None):
        if type(commands) == tuple:
            actions = commands
        else:
            self.inputFile = commands
            actions = ()

        self.ReadToPrompt()

        t = 1
        completed_actions = []
        self.Start()
        while not self.quitting:
            if t < len(actions):
                commandStr = actions[t]
                self.Output(self.prompt + commandStr)
            else:
                commandStr, expectedMessage = self.Input(self.prompt)

            preTickMessage, preTickResult = self.PreTick()
            if preTickMessage is not None and preTickMessage != "":
                preTickMessage = '\n' + preTickMessage
                self.Output(preTickMessage)
                message += preTickMessage

            t += 1

            if preTickResult == Response.QuestCompleted:
                self.End()

            if commandStr != "":
                message, result, action = self.Do(commandStr)
                completed_actions += action
                if expectedMessage=="":
                    expectedMessage = self.ReadToPrompt() # Occurs when a question is prompted after the command

            postTickMessage, postTickResult = self.PostTick()
            if postTickMessage is not None and postTickMessage != "":
                postTickMessage = '\n' + postTickMessage
                self.Output(postTickMessage)
                message += postTickMessage

            if result == Response.QuestCompleted or postTickResult == Response.QuestCompleted:
                self.End()

            if steps is not None and t > steps:
                self.End()

            self.ValidateOutput(expectedMessage, message)

        if self.state.isDead:
            self.Output("I'M DEAD!\nYOU DIDN'T WIN")

        if self.inputFile is not None:
            self.inputFile.close()

    def Start(self, game):
        pass

    def End(self):
        self.Output("Your quest is completed!")
        if self.Input("WOULD YOU LIKE TO TRY AGAIN (Y/N)")[0] == 'Y':
            self.NewGame()
            self.Start()
            t = 0
        else:
            self.quitting = True

    def PreTick(self):
        return "", Response.Success

    def PostTick(self):
        return "", Response.Success

    def PreCommand(self, verb, target):
        return "", Response.Success

    def BaseVerb(self, verbStr):
        if verbStr in self.world.verbs:
            verb = self.world.verbs[verbStr]
        else:
            verb = BuiltInVerbs.builtinVerbsList[verbStr]
        return verb

    def Look(self, at=None):
        return self.BaseVerb('LOOK').Do(at, self)

    def GoTo(self, location):
        self.state.location = self.world.ResolveLocation(location)

    def CreateHere(self, object):
        object = self.world.ResolveObject(object)
        self.MoveObject(object, self.state.location)

    def CreateMine(self, object):
        object = self.world.ResolveObject(object)
        self.CreateHere(object)
        self.state.inventory.Add(object)

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
        for location in MakeTuple(location):
            if self.state.location == self.world.ResolveLocation(location):
                return True
        return False

    def ObjectAtLocation(self, object, location):
        object = self.world.ResolveObject(object)
        location = self.world.ResolveLocation(location)
        if type(object.placement) == LocationPlacement:
            return object.placement.location == location
        return False

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
        """Print an error if the input messages don't match"""
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

    def Trim(self, commands, steps):
        """Simplify the game by removing any objects, locations, or verbs not seen
        after running the input command sequence for the specified number of steps.

        Warning: It takes some care to ensure that all potentially visible items have been
        seen in the specified number of steps. For example, all accessible rooms should be visited. """
        self.Run(commands, steps)
        for object in self.world.objects:
            if not object.seen:
                self.startingWorld.objects.Remove(object.name)
        for location in self.world.locations:
            if not location.seen:
                self.startingWorld.locations.Remove(location.name)
        for verb in self.world.verbs:
            if not verb.seen:
                self.startingWorld.verbs.Remove(verb.name)
