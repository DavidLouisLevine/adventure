from adventure.direction import Direction
from adventure.response import Response

class Verbs:
    def __init__(self, verbs):
        self.items = verbs
        i = 1
        for item in self.items:
            item.index = i
            i += 1

    def __getitem__(self, item):
        if type(item) is str:
            for i in range(len(self.items)):
                item2 = self.items[i]
                if item2.name == item or item2.abbreviation[:3] == item[:3]:
                    return self.items[i]
            return None
        else:
            return self.items[item - 1]

    def len(self):
        return len(self.items)

    def Do(self, target, game):
        raise NotImplementedError()

class Verb:
    # If both targetInventory and targetInRoom are False then there are no restrictions on the target location
    # If either is True then only targets in those locations are allowed.
    def __init__(self, name, abbreviation, targetNever=False, targetOptional=False, targetInventory=True, targetInRoom=True):
        self.name = name
        self.abbreviation = abbreviation
        self.targetNever = targetNever
        self.targetOptional = targetOptional
        self.targetInventory = targetInventory
        self.targetInRoom = targetInRoom
        self.index = None

    def Do(self, target, game):
        #assert (target is None or target.IsObject())
        return self.DoObject(target, game)

    def MakeResponse(self, f=None, *args, **kwargs):
        return Response(self.index, f, *args, **kwargs)

    def __str__(self):
        return self.name

class GoVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def Do(self, target, game):
        m = ""
        cant = "I CAN'T GO THAT WAY AT THE MOMENT."
        currentLocation = game.state.location
        if target.IsDirection():
            move = game.state.location.moves[target.value.d]
            if move == 0:
                return "I CAN'T GO THAT WAY AT THE MOMENT."
            game.state.location = game.world.locations[move]
            m = ""
        elif target.IsObject():
            object = target.value
            if game.state.location == object.placement.location:
                if object.responses is not None:
                    m = Response.Respond(object.responses, self.index, game)
                    if m is None:
                        return cant
                    if m != "":
                        pass # m = m + "\n"
                else:
                    return cant
            else:
                return "I DON'T SEE THAT HERE."
        return m

class DropVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if game.state.inventory.Remove(target.value, game.state.location):
            return "O.K. I DROPPED IT."
        else:
            return "I DON'T SEEM TO BE CARRYING IT."

class GetVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        object = target.value
        if object.placement.location == game.state.location:
            m = None
            if object.moveable and object.responses is not None:
                m = Response.Respond(object.responses, self.index, game)
            if not object.moveable:
                m = "I CAN'T CARRY THAT!"
            elif game.state.inventory.Has(object):
                m = "I ALREADY HAVE IT."
            elif game.state.inventory.capacity == len(game.state.inventory.Get(game.world)):
                m = "I CAN'T CARRY ANYMORE."
            else:
                game.state.inventory.Add(object)
                m = "O.K."
        else:
            m = "I DON'T SEE THAT HERE."
        return m

def CanGet(game, *args, **kwargs):
    return ""

class InventoryVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        m = "WE ARE PRESENTLY CARRYING:\n"
        objects = game.state.inventory.Get(game.world)
        if len(objects) == 0:
            m += "NOTHING"
        else:
            first = True
            for object in game.state.inventory.Get(game.world):
                if not first:
                    m += "\n"
                    first = False
                m += object.name
        return m

class LookVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        m = "WE ARE " + game.state.location.name + "."
        if target is not None and target.IsObject():
            object = target.value
            if object.responses is not None:
                m = Response.Respond(object.responses, self.index, game)
                if m is None or m == "":
                    print("I SEE NOTHING OF INTEREST.")
        else:
            for object in game.world.AtLocation(game.state.location):
                if object.visible:
                    if not m == "":
                        m += "\n"
                    m += "I CAN SEE " + object.name + "."
            moves = game.state.location.moves
            if moves.count(0) != len(moves):
                if not m == "":
                    m += "\n"
                m += "WE COULD EASILY GO: "
                for i in range(len(moves)):
                    if moves[i] != 0:
                        m += Direction.names[i] + "  "
            else:
                m += "\n"
            m += "\n>" + '-' * 62 + "<"
        return m

class QuitVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        m = "WHAT? YOU WOULD LEAVE ME HERE TO DIE ALONE?\n"
        m += "JUST FOR THAT, I'M GOING TO DESTROY THE GAME.\n\n\n\nBOOOOOOOOOOOOM!"
        game.quitting = True
        return m

class BuiltInVerbs(Verbs):
    def __init__(self, verbs):
        Verbs.__init__(self, BuiltInVerbs.builtinVerbs + verbs)

    builtinVerbs = (
        (GoVerb('GO', 'GO ')),
        (GetVerb('GET', 'GET')),
        (DropVerb('DROP', 'DRO')),
#        (DropVerb('DROP', 'DRO', targetInventory=False, targetInRoom=False)),
        (LookVerb('LOOK', 'LOO', targetOptional=True)),
        (QuitVerb('QUIT', 'QUI', targetNever=True)),
        (InventoryVerb('INVENTORY', 'INV', targetNever=True))
    )