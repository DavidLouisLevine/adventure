from adventure.response import Response
from adventure.item import Items, Item

class Objects(Items):
    def __init__(self, objects):
        Items.__init__(self, objects)

class Object(Item):
    def __init__(self, name, abbreviation, placement, response=None, moveable=False, visible=True):
        Item.__init__(self, name, abbreviation)
        self.placement = placement
        self.responses = response
        self.moveable = moveable
        self.visible = visible

    def Responses(self, verb=None):
        if self.responses is None:
            responses = ()
        elif type(self.responses) is Response:
            responses = (self.responses, )
        else:
            responses = self.responses

        return filter(lambda x: x.verb == verb, responses)

    def __str__(self):
        return self.abbreviation