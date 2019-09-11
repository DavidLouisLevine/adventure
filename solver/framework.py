#from cia.cia_game import CIA
from home.home_game import Home
from adventure.direction import Direction
from adventure.target import Target
from adventure.response import Response
import adventure.util as util

# This class supports the methods in the MIT x6.86 framework class

DEFAULT_REWARD = -0.01 # Negative reward for each non-terminal step
JUNK_CMD_REWARD = -0.1 # Negative reward for invalid commands
QUEST_REWARD = 1 # positive reward for finishing quest
STEP_COUNT = 0  #count the number of steps in current episode
MAX_STEPS = 20

#game = CIA()
game = Home()
game.Init()

def load_game_data():
    pass

def get_actions():
    return game.world.verbs.GetAbbreviations()

def get_objects():
    return game.world.objects.GetAbbreviations() + ['NORTH', 'SOUTH', 'EAST', 'WEST']

def get_descriptions():
    names = ()
    for location in game.world.locations:
        names +=  util.MakeTuple((location.name, ))

    return names

num_actual_objects = len(game.world.objects)
num_actions = len(game.world.verbs)

def newGame():
    global STEP_COUNT
    STEP_COUNT = 0
    return game.NewGame((get_action_index('eat'), get_object_index('apple')))
#    current = game.NewGame(random.choice(range(num_acu)))

def step_game(current_room_desc, current_quest_desc, action_index, object_index):
    global STEP_COUNT
    STEP_COUNT = STEP_COUNT+1
    terminal = (STEP_COUNT >= MAX_STEPS)

    verb = game.world.verbs[int(action_index)]
    objects = get_objects()
    object_index = int(object_index)
    if object_index >= len(objects) - 4:
        target = Target(Direction(objects[object_index]))
    else:
        target = Target(game.world.objects[object_index])
    message, reward, result = game.DoTarget(verb, target)

    terminal = terminal or result in (Response.Fatal, Response.CompletedQuest)

    if result == Response.IllegalCommand:
        reward = JUNK_CMD_REWARD + DEFAULT_REWARD
    elif result == Response.CompletedQuest:
        reward = QUEST_REWARD
        terminal = True
    else:
        reward = DEFAULT_REWARD

    next_room_desc = game.state.location.Name()
    #print(get_action_name(action_index), get_object_name(object_index), '->', next_room_desc, reward, result, message)

    return next_room_desc, get_quest_name(), reward, terminal

def get_action_name(action_index):
    return game.world.verbs[int(action_index)].abbreviation

def get_action_index(action_name):
    return game.world.verbs[action_name].i

def get_object_name(object_index):
    objects = get_objects()
    if object_index >= len(objects) - 4:
        return Direction(object_index - len(objects) + 4).Name()
    else:
        return game.world.objects[int(object_index)].abbreviation

def get_object_index(object_name):
    return game.world.objects[object_name].i

def get_quest_name():
    return game.QuestName()
