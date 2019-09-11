from adventure.placement import NoPlacement, AtLargePlacement
from adventure.object import Object
from adventure.response import Response
from home.home_verb import eat, sleep, go, watch, exercise

objects = (
    Object('apple', 'apple', 'Kitchen', (eat(ifAtLocation='Kitchen', reward=1), eat(result=Response.IllegalCommand))),
    Object('tv', 'tv', 'Living', (watch(ifAtLocation='Living', reward=1), watch(result=Response.IllegalCommand))),
    Object('bike', 'bike', 'Garden', (exercise(ifAtLocation='Garden', reward=1), watch(result=Response.IllegalCommand))),
    Object('bed', 'bed', 'Bedroom', (sleep(ifAtLocation='Bedroom', reward=1), watch(result=Response.IllegalCommand))),
)