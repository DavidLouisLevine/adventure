from adventure.placement import NoPlacement
from adventure.object import Object
from adventure.response import Response
from home.home_verb import eat, sleep, go, watch, exercise

completedMessage = 'Congratulations!'

objects = (
    Object('an apple', 'apple', 'Kitchen', (
        eat(ifAtLocation='Kitchen', ifEQ=('quest', 'eat apple'), message=completedMessage, result=Response.QuestCompleted),
        eat(ifAtLocation='Kitchen', message="Crispy and sweet!", result=Response.IllegalCommand),
        eat(result=Response.IllegalCommand))),
    Object('a tv', 'tv', 'Living', (
        watch(ifAtLocation='Living', ifEQ=('quest', 'watch tv'), message=completedMessage,  result=Response.QuestCompleted),
        watch(ifAtLocation='Living', message="Not much to see.", result=Response.IllegalCommand),
        watch(result=Response.IllegalCommand))),
    Object('a bike', 'bike', 'Garden', (
        exercise(ifAtLocation='Garden', ifEQ=('quest', 'exercise bike'), message=completedMessage, result=Response.QuestCompleted),
        exercise(ifAtLocation='Garden', message="Spin, spin spin!", result=Response.IllegalCommand),
        exercise(result=Response.IllegalCommand))),
    Object('a bed', 'bed', 'Bedroom', (
        sleep(ifAtLocation='Bedroom', ifEQ=('quest', 'sleep bed'), message=completedMessage, result=Response.QuestCompleted),
        sleep(ifAtLocation='Bedroom', message="Zzzzzzzz....", result=Response.IllegalCommand),
        sleep(result=Response.IllegalCommand))),
)