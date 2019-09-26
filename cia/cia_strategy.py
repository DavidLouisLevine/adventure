from adventure.response import Response
from adventure.placement import LocationPlacement
import adventure.util as util

from solve.strategy import Strategy

class CIAStrategy(Strategy):
    def __init__(self, game):
        super().__init__(game)

    def get_state(self, current_room_desc):
        locations = []
        for location in self.game.world.locations:
            if location.seen:
                locations += [self.make_seen_name(location.abbreviation)]
        return ' '.join((
                current_room_desc,
                ' '.join(map(lambda x:self.make_inventory_name(x), self.get_inventory_strings())),
                self.get_look_string(self.game.state.location),
                ' '.join(locations)))
                #self.game.questName))

    def move_allowed(self, action_index, object_index):
        if object_index >= len(self.game.world.objects.index):
            if action_index == 0 and self.game.AtLocation('LOBBY'):
                jj = 9
            return action_index == self.game.world.verbs['GO'].i
        if action_index in (self.game.world.verbs['QUIT'].i, self.game.world.verbs['INV'].i):
            return False
        return self.game.IsHere(object_index)

    def get_descriptions(self):
        names = ()
        for location in self.game.world.locations:
            for name in util.MakeTuple(location.name):
                names +=  (util.MakeTuple(name), )
            names += (util.MakeTuple(self.make_seen_name(location.abbreviation)),)
            # for response in util.MakeTuple(location.responses):
            #     if response.HasArg('message'):
            #         names += (util.MakeTuple(response.Arg('message')), )

        for object in self.game.world.objects:
            names += (util.MakeTuple(self.make_inventory_name(object.abbreviation)), )

        look_string = self.get_look_string()
        if look_string != '':
            names += (util.MakeTuple(look_string), )

        return names

    def make_seen_name(self, name):
        return 'SEEN' + name

    def make_inventory_name(self, name):
        return 'INV' + name

    def get_inventory_strings(self):
        return self.game.state.inventory.GetStrings(self.game.world)

    def has_conditional_look_response(self, responses):
        for response in Response.Responses(responses, self.game.world.verbs['LOOK']):
            if response.is_conditional_look_response():
                return True
        return False

    # For objects that are in the room and a conditional response to the LOOK command
    # (with no result arg or result=Response.Success),
    # return the message of the response that currently applies.
    #
    # When location is None, we gather all such strings instead
    def get_look_string(self, location=None):
        looks = []
        for object in self.game.world.objects:
            if self.has_conditional_look_response(object.responses):
                if location is None:
                    for response in Response.Responses(object.responses, self.game.world.verbs['LOOK']):
                        looks += [response.kwargs['message']]
                elif type(object.placement) == LocationPlacement and object.placement.location == location:
                    message, reward, result = Response.Respond(object.responses, self.game.world.verbs['LOOK'], self.game)
                    if result == Response.Success:
                        looks += [message, ]
        return ' '.join(looks)