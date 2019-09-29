from adventure.direction import Direction
from adventure.direction import Direction
from adventure.target import Target
from adventure.response import Response
from adventure.placement import LocationPlacement
from adventure.util import MakeTuple
import adventure.util as util


# This class supports the methods in the MIT x6.86 framework class

STEP_COUNT = 0  #count the number of steps in current episode
MAX_STEPS = 20  #number of steps in an espisode

game = None
num_actual_objects = None   # Doesn't include Directions
num_objects = None          # Includes directions
num_actions = None

# These seen things are global for the entire solution sequence.
seen_locations = None
seen_objects = None

fresh_epoch = None

def ready():
    return game is not None

def load_game_data(g):
    global num_actions, num_actual_objects, num_objects, game, seen_locations, seen_objects, fresh_epoch
    game = g
    game.Init()
    num_actual_objects = len(game.world.objects.index) # Don't include NORTH, SOUTH, EAST, WEST
    num_objects = num_actual_objects + 4
    num_actions = len(game.world.verbs)
    seen_locations = [False, ] * len(game.world.locations)
    seen_objects = [False, ] * num_actual_objects
    fresh_epoch = True

def new_epoch():
    global fresh_epoch
    fresh_epoch = True

def get_actions():
    return game.world.verbs.GetAbbreviations()

def get_objects():
    return game.world.objects.GetAbbreviations() + ['NORTH', 'SOUTH', 'EAST', 'WEST']

def new_game(maxSteps=None):
    global STEP_COUNT, MAX_STEPS, num_actions, num_actual_objects, num_objects
    STEP_COUNT = 0
    if maxSteps is not None:
        MAX_STEPS = maxSteps
    ng =  game.NewGame()
    num_actual_objects = len(game.world.objects.index) # Don't include NORTH, SOUTH, EAST, WEST
    num_objects = num_actual_objects + 4
    num_actions = len(game.world.verbs)
    game.UpdateSeen(None)
    return ng

def update_seen():
    global fresh_epoch
    if not seen_locations[game.state.location.i]:
        if fresh_epoch:
            #print("")
            fresh_epoch = False
        #print("SEEN LOCATION:", game.state.location)
        seen_locations[game.state.location.i] = True

    for object in game.world.objects:
        if object.seen and not seen_objects[object.i]:
            if fresh_epoch:
                #print("")
                fresh_epoch = False
            #print("SEEN OBJECT:", object)
            seen_objects[object.i] = True

def step_game(current_room_desc, current_quest_desc, action_index, object_index):
    global STEP_COUNT, fresh_epoch
    STEP_COUNT = STEP_COUNT+1
    terminal = (STEP_COUNT >= MAX_STEPS)

    if action_index == game.world.verbs['GO'].i and 'BUILDING' in game.world.objects and object_index == game.world.objects['BUILDING'].i:
        jj = 9

    verb = game.world.verbs[int(action_index)]
    objects = get_objects()
    object_index = int(object_index)
    if object_index >= len(objects) - 4:
        target = Target(Direction(objects[object_index]))
    else:
        target = Target(game.world.objects[object_index])

    message, reward, result = game.DoTarget(verb, target)

    terminal = terminal or result in (Response.Fatal, Response.QuestCompleted)

    update_seen()

    reward = reward + game.rewards[result]

    next_room_desc = game.state.location.Name()
    #print(get_action_name(action_index), get_object_name(object_index), '->', next_room_desc, current_quest_desc, reward, result, message)

    if game.state.location == game.world.locations['LOBBY']:
        #print("LOBBY reward:", reward)
        jj = 9

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
    return game.questName

def get_success_reward():
    return game.rewards[Response.Success]