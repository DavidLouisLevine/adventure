import adventure.util as util

from solve.strategy import Strategy

class HomeStrategy(Strategy):
    def __init__(self, game):
        super().__init__(game)

    def get_state(self, current_room_desc):
        return ' '.join((current_room_desc, self.game.questName))

    def move_allowed(self, action_index, object_index):
        return True

    def get_descriptions(self):
        names = ()
        for location in self.game.world.locations:
            for name in util.MakeTuple(location.name):
                names +=  (util.MakeTuple(name), )

        for quest in self.game.questNames:
            names += (util.MakeTuple(quest), )

        return names
