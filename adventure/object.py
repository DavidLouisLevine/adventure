from adventure.response import Response
from adventure.item import Items, Item
from adventure.placement import InventoryPlacement

# Things in the world
class Objects(Items):
    def __init__(self, objects):
        Items.__init__(self, objects)

    def Find(self, item, location=None):
        i = None
        if type(item) == str:
            abbreviation = Items.Abbreviate(item)
            for ii in self.index:
                if (ii.name == item or Items.Abbreviate(ii.abbreviation) == abbreviation) and\
                        (location is None or ii.placement.location == location or type(ii.placement) == InventoryPlacement):
                    i = ii
                    break
        elif type(item) == int:
            i = self.index[item]

        return i

# One thing in the world
class Object(Item):
    def __init__(self, name, abbreviation, placement, responses=None, moveable=False, visible=True):
        super().__init__(name, abbreviation)
        self.placement = placement
        self.responses = responses
        self.moveable = moveable
        self.visible = visible

    # Returns all responses matching verb
    def Responses(self, verb=None):
        if self.responses is None:
            responses = ()
        elif type(self.responses) is Response:
            responses = (self.responses, )
        else:
            responses = self.responses

        return responses if verb is None else filter(lambda x: x.verb == verb, responses)

    def __str__(self):
        return self.abbreviation