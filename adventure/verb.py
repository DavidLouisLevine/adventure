from adventure.direction import Direction
from adventure.response import Response
from adventure.item import Items, Item
from adventure.placement import InventoryPlacement
from adventure.util import MakeTuple

class Verbs(Items):
    def __init__(self, objects):
        Items.__init__(self, objects)

    def Do(self, target, game):
        raise NotImplementedError()

class Verb(Item):
    # If both targetInventory and targetInRoom are False then there are no restrictions on the target location
    # If either is True then only targets in those locations are allowed.
    def __init__(self, name, abbreviation, targetNever=False, targetOptional=False, targetInventory=True, targetInRoom=True):
        Item.__init__(self, name, abbreviation)
        self.targetNever = targetNever
        self.targetOptional = targetOptional
        self.targetInventory = targetInventory
        self.targetInRoom = targetInRoom
        self.responses = ()

    def Do(self, target, game):
        #assert (target is None or target.IsObject())
        return self.DoObject(target, game)

    def MakeResponse(self, f=None, *args, **kwargs):
        return Response(self, f, *args, **kwargs)

    def __str__(self):
        return self.name

class ResponseVerb(Verb):
    def __init__(self, name, abbreviation, responses=None, *args, **kwargs):
        # The superclass isn't expecting these arguments
        if 'notApplicableMessage' in kwargs:
            self.notApplicableMessage = kwargs.pop('notApplicableMessage')
        else:
            self.notApplicableMessage = None
        if 'didntWorkMessage' in kwargs:
            self.didntWorkMessage = kwargs.pop('didntWorkMessage')
        else:
            self.didntWorkMessage = None

        super().__init__(name, abbreviation, *args, **kwargs)

        if responses is not None:
            self.responses = MakeTuple(responses)
            for response in self.responses:
                response.verb = self
        else:
            self.responses = None

    def DoObject(self, target, game):
        m, reward, result = "", 0, Response.IllegalCommand

        # Process responses from the verb
        if Response.HasResponse(self.responses, self):
            m, reward, result = Response.Respond(self.responses, self, game,
                                                 target.value if target is not None and target.IsObject() else None)
            if m is not None and m != "":
                return m, reward, result

        # Process responses from the object
        if target is not None and target.IsObject() and Response.HasResponse(target.value.responses, self):
            m, reward, result = Response.Respond(target.value.responses, self, game)
            if m is None or m == "":
                m = self.didntWorkMessage
                result = Response.IllegalCommand
        elif self.notApplicableMessage is not None:
            m = self.notApplicableMessage
            result = Response.IllegalCommand
        return m, reward, result

def VerbResponse(*args, **kwargs):
    return Response(None, None, *args, **kwargs)

class GoVerb(Verb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def Do(self, target, game):
        m, reward, result = "", 0, Response.IllegalCommand
        cant = "I CAN'T GO THAT WAY AT THE MOMENT."
        if target.IsDirection():
            move = game.state.location.moves[target.value.d]
            if move == 0:
                return cant, 0, Response.IllegalCommand
            game.state.location = game.world.locations[move]
            m = ""
            result = Response.Success
        elif target.IsObject():
            object = target.value
            if game.state.location == object.placement.location:
                if Response.HasResponse(object.responses, self):
                    m, reward, result =  Response.Respond(object.responses, self, game)
                    if not Response.IsSuccessfulResult(result) and (m is None or m == ""):
                        return cant, 0, Response.IllegalCommand
                else:
                    return cant, 0, Response.IllegalCommand
            else:
                return "I DON'T SEE THAT HERE.", 0, Response.IllegalCommand
        return m, reward, result

class DropVerb(Verb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject() and game.state.inventory.Remove(target.value):
            game.CreateHere(target.value)
            m = ""
            if target.IsObject() and Response.HasResponse(target.value.responses, self):
                m, reward, result = Response.Respond(target.value.responses, self, game)
            if m == "":
                return "O.K. I DROPPED IT.", 0, Response.Success
            else:
                return m, reward, result
        else:
            return "I DON'T SEEM TO BE CARRYING IT.", 0, Response.IllegalCommand

class GetVerb(Verb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def DoObject(self, target, game):
        object = target.value
        m, reward, result = "", 0, Response.IllegalCommand
        if target.IsObject() and\
                (type(object.placement) == InventoryPlacement or object.placement.location == game.state.location):
            m = None
            if not object.moveable:
                m = "I CAN'T CARRY THAT!"
            elif game.state.inventory.Has(object):
                m = "I ALREADY HAVE IT."
                result = Response.Success
            elif game.state.inventory.capacity == len(game.state.inventory.Get(game.world)):
                m = "I CAN'T CARRY ANYMORE."
            elif object.moveable:
                if Response.HasResponse(object.responses, self):
                    m, reward, result = Response.Respond(object.responses, self, game)
                game.state.inventory.Add(object)
                if m is None:
                    m = ""
                if m != "":
                    m = '\n' + m
                m = "O.K." + m
                result = Response.MightBeUseful
        else:
            m = "I DON'T SEE THAT HERE."
        return m, reward, result

class InventoryVerb(Verb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def DoObject(self, target, game):
        m = "WE ARE PRESENTLY CARRYING\n"
        objects = game.state.inventory.Get(game.world)
        if len(objects) == 0:
            m += "NOTHING"
        else:
            first = True
            for object in game.state.inventory.Get(game.world):
                if not first:
                    m += "\n"
                else:
                    first = False
                m += object.name + " "
        return m, 0, Response.NotUseful

class LookVerb(Verb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def DoObject(self, target, game):
        m, reward, result = "", 0, Response.IllegalCommand
        if target is not None and target is not '' and target.IsObject():
            object = target.value
            m = None
            if object.responses is not None:
                m, reward, result = Response.Respond(object.responses, self, game)
            if m is None or m == "":
                m = "I SEE NOTHING OF INTEREST."
        else:
            m = "WE ARE " + game.state.location.Name() + "."
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
        return m, reward, Response.NotUseful

class QuitVerb(Verb):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def DoObject(self, target, game):
        m = "WHAT? YOU WOULD LEAVE ME HERE TO DIE ALONE?\n"
        m += "JUST FOR THAT, I'M GOING TO DESTROY THE GAME.\n\n\n\nBOOOOOOOOOOOOM!"
        game.quitting = True
        return m, 0, Response.Fatal

class BuiltInVerbs(Verbs):
    def __init__(self, verbs, f=None):
        filtered = BuiltInVerbs.builtinVerbs if f is None else list(filter(lambda x:x.abbreviation in f, BuiltInVerbs.builtinVerbs))
        Verbs.__init__(self, list(filtered) + list(verbs))

    builtinVerbs = (
        (GoVerb('GO', 'GO')),
        (GetVerb('GET', 'GET')),
        (DropVerb('DROP', 'DRO')),
        (LookVerb('LOOK', 'LOO', targetOptional=True)),
        (QuitVerb('QUIT', 'QUI', targetNever=True)),
        (InventoryVerb('INVENTORY', 'INV', targetNever=True))
    )

    builtinVerbsList = Verbs(builtinVerbs)