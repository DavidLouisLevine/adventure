# Custom interface between the framework and the game

class Strategy:
    def __init__(self, game):
        self.game = game

    # Return a vector that represents the current state based on self.game and the current room description
    # We can't just get the description from self.game because there are multiple descriptions for the same room
    def get_state(self, current_room_desc):
        pass

    # Get a list of strings that encompass all of the possible outputs of the game
    def get_descriptions(self):
        pass

    # Return True if the move is grossly legal (e.g. if the object is in the current location, if SOUTH is only used with GO)
    def move_allowed(self, action_index, object_index):
        pass
