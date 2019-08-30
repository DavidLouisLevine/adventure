from location import LocationPlacement, InventoryPlacement, Locations
from verb import BuiltInVerbs
from object import Objects, Target
from direction import Direction
import numpy as np
import response

class Game:
    def __init__(self, world, state):
        self.world = world
        self.state = state
        self.quitting = False
        self.inputFile = open("ciatest.adv", "r")
        self.inResponse = False

    def Input(self, prompt):
        if self.inputFile is not None:
            print(prompt + '? ', end='')
            u = ""
            while u == "":
                #k = self.inputFile.readlines()
                t = self.inputFile.readline()
                if t == "":
                    break
                if t[0] != '#':
                    u = t

            message = ""
            while True:
                t = self.inputFile.readline()
                if t == "":
                    break

                if t[:4] == '---@':
                    break

                if t[0] != '#':
                    message += t

            if t == "":
                self.inputFile.close()
                self.inputFile = None

            if u != "":
                print(u, end='')
                return (u, message)

        if self.inputFile is None:
            return (input(prompt), None)

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
                if expectedMessage is not None and expectedMessage != actualMessage:
                    print("ERROR: Expected Message:\n", expectedMessage)
                    print("ERROR: Actual Message:\n", actualMessage)
                    n = min(len(actualMessage), len(expectedMessage))
                    k = np.array(list(expectedMessage[:n])) == np.array(list(actualMessage[:n]))
                    j = 1
            else:
                if expectedMessage is not None and expectedMessage != "":
                    print("ERROR: Actual message is empty but expected message is:", expectedMessage)

            self.Tick()
            t += 1

    def Tick(self, target, game):
        pass

    def Look(self):
        return self.world.verbs['LOOK'].Do(None, self)

class World:
    def __init__(self, objects, verbs):
        self.locations = Locations()
        self.verbs = verbs
        self.objects = Objects(objects)
        for object in self.objects:
            if type(object.placement) is int:
                object.placement = LocationPlacement(self.locations[object.placement])

    def AtLocation(self, location):
        l = ()
        for object in self.objects:
            if type(object.placement) is LocationPlacement and object.placement.location == location:
                l += (object, )
        return l

    def print(self):
        s = ""
        for i in range(self.locations.len()):
            print(i + 1, self.locations[i + 1].name, self.locations[i + 1].moves)

        for i in range(self.objects.len()):
            o = self.objects[i]
            print(i, o.name, o.placement)

        for i in range(self.verbs.len()):
            print(i, self.verbs[i].name)

class State:
    def __init__(self, location, world):
        self.location = location
        self.inventory = Inventory(5, self, world)

class Inventory:
    def __init__(self, capacity, state, world):
        self.capacity = capacity
        self.size = 0
        self.state = state
        self.world = world

    def Get(self):
        items = ()
        for object in self.world.objects:
            if object.placement.InInventory():
                items += (object, )
        return items

    def Has(self, object):
        return object.placement.InInventory()

    def Add(self, object):
        if self.size != self.capacity:
            object.placement = InventoryPlacement()
            self.size += 1
            assert(self.size <= self.capacity)
            return True
        else:
            return False

    def Remove(self, object, location):
        if self.Has(object):
            object.placement = LocationPlacement(location)
            self.size -= 1
            assert(self.size >= 0)
            return True
        else:
            return False
