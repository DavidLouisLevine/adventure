from cia.cia_game import CIA
from adventure.world import World
from adventure.direction import Direction
from adventure.target import Target

# This class mimics the methods in the  MIT x6.86 framework class

game = CIA()
game.Init()

def load_game_data():
    pass

def get_actions():
    return game.world.verbs.GetAbbreviations()

def get_objects():
    return game.world.objects.GetAbbreviations() + ['NORTH', 'SOUTH', 'EAST', 'WEST']

def get_descriptions():
    return game.world.objects.GetNames()

def newGame():
    return game.NewGame("GO BUILDING")

def step_game(current_room_desc, current_quest_desc, action_index, object_index):
    verb = game.world.verbs[int(action_index)]
    objects = get_objects()
    object_index = int(object_index)
    if object_index > len(objects) - 4:
        target = Target(Direction(objects[object_index]))
    else:
        target = Target(game.world.objects[object_index])
    message = game.DoTarget(verb, target)
    return message, game.quest, 0, False
