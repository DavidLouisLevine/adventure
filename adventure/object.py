import copy
from adventure.response import Response
from adventure.items import Items

class Objects(Items):
    def __init__(self, objects):
        Items.__init__(self, objects)

class Object:
    def __init__(self, name, abbreviation, placement, response=None, moveable=False, visible=True):
        self.name = name
        self.abbreviation = abbreviation
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