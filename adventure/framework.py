from adventure.world import World

# This class mimics the methods in the  MIT x6.86 framework class

class framework:
    def __init__(self, game):
        self.game = game

    def get_actions(self):
        return self.world.verbs.GetStrings()


    def get_objects(self):
        return self.world.objects.GetStrings()


    def newGame(self):
        return