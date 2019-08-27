class Verb:
    def __init__(self, name, abbreviation):
        self.name = name
        self.abbreviation = abbreviation

class ObjectVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def Do(self, target, game):
        #assert (target is None or target.IsObject())
        return self.DoObject(target, game)

class Verbs:
    def __init__(self, verbs):
        self.items = verbs

    def __getitem__(self, item):
        if type(item) is str:
            for i in range(len(self.items)):
                if self.items[i].name == item:
                    return self.items[i]
            return None
        else:
            return self.items[item - 1]

    def len(self):
        return len(self.items)

    def Do(self, target, game):
        raise NotImplementedError()

class GoVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def Do(self, target, game):
        m = ""
        if target.IsDirection():
            move = game.state.location.moves[target.value.d]
            if move == 0:
                return "I CAN'T GO THAT WAY AT THE MOMENT."
            game.state.location = game.world.locations[move]
            m = ""
        elif target.IsObject():
            object = target.value
            if game.state.location == object.placement.location:
                #if object.response.verb == 1:
                    #print("WE ARE", self.state.location.name)
                    if object.response is not None and object.response.f is not None:
                        m = object.response.f(game.state, game.world)
                        m = m + "\n" if not m is None else ""
        m += "WE ARE " + game.state.location.name + "\n"

        m += game.Look()
        return m

class DropVerb(ObjectVerb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        game.state.inventory.Remove(target.value, game.state.location)

class GetVerb(ObjectVerb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        object = target.value
        if object.placement.location == game.state.location:
            if not object.moveable:
                m = "I CAN'T CARRY THAT!"
            elif game.state.inventory.Has(object):
                m = "I ALREADY HAVE IT."
            elif game.state.inventory.capacity == len(game.state.inventory.Get()):
                m = "I CAN'T CARRY ANYMORE."
            else:
                game.state.inventory.Add(object)
                m = "O.K."
        else:
            m = "I DON'T SEE THAT HERE."
        return m

class InventoryVerb(ObjectVerb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        m = "WE ARE PRESENTLY CARRYING:\n"
        objects = game.state.inventory.Get()
        if len(objects) == 0:
            m += "NOTHING"
        else:
            first = True
            for object in game.state.inventory.Get():
                if not first:
                    m += "\n"
                    first = False
                m += object.name
        return m

class LookVerb(ObjectVerb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        m = ""
        objects = game.world.AtLocation(game.state.location)
        for object in objects:
            if object.lookable:
                if not m == "":
                    m += "\n"
                m += "I CAN SEE " + object.name
        return m

class BuiltInVerbs(Verbs):
    def __init__(self, verbs):
        Verbs.__init__(self, BuiltInVerbs.builtinVerbs + verbs)

    builtinVerbs = (
        (GoVerb('GO', 'GO ')),
        (GetVerb('GET', 'GET')),
        (DropVerb('DROP', 'DRO')),
        (LookVerb('LOOK', 'LOO')),
        (Verb('QUIT', 'QUI')),
        (InventoryVerb('INVENTORY', 'INV'))
    )