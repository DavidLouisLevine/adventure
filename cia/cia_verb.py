from adventure.response import Response
from adventure.verb import Verb, BuiltInVerbs, ResponseVerb, VerbResponse
from adventure.util import MakeTuple
from adventure.target import Target

class PushVerb(ResponseVerb):
    def __init__(self, name, abbreviation, responses=None, *args, **kwargs):
        super().__init__(name, abbreviation, responses, *args, **kwargs)

    def DoObject(self, target, game):
        # The original game logic says that "BUT" always refers to the box button when it is possessed
        if target is not None and target.IsObject() and target.value.abbreviation[:3] == "BUT":
            if game.Has('BOX'):
                target = Target(game.world.objects['A BUTTON ON A BOX'])
                m, reward, result = Response.Respond(target.value.responses, self, game)
                return m, reward, result
        return super().DoObject(target, game)

customVerbs = (
    PushVerb('PUSH', 'PUS', (
        VerbResponse(ifNotHere=True, message="I DON'T SEE THAT HERE.", result=Response.IllegalCommand),
        VerbResponse(ifNoObjectResponse=True, message="NOTHING HAPPENS.", result=Response.IllegalCommand))),
    ResponseVerb('PULL', 'PUL', VerbResponse(ifNoObjectResponse=True, message="NOTHING HAPPENS.", result=Response.IllegalCommand)),
    ResponseVerb('INSERT', 'INS',(
        VerbResponse(ifNotHere=True, message="I DON'T SEE THAT HERE.", result=Response.IllegalCommand),
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T INSERT THAT!", result=Response.IllegalCommand)),
        didntWorkMessage="NOTHING HAPPENED."),
    ResponseVerb('OPEN', 'OPE', (
        VerbResponse(ifNotHere=True, message="I CAN'T OPEN THAT!", result=Response.IllegalCommand),
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T OPEN THAT!", result=Response.IllegalCommand)),
        didntWorkMessage="I CAN'T DO THAT......YET!"),
    ResponseVerb('WEAR', 'WEA', (
        VerbResponse(ifNotHas=True, message="I CAN'T WEAR THAT!", result=Response.IllegalCommand),
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T WEAR THAT!", result=Response.IllegalCommand))),
    ResponseVerb('READ', 'REA', (
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T READ THAT!", result=Response.IllegalCommand),
        VerbResponse(ifNotHere=True, message="I DON'T SEE THAT HERE.", result=Response.IllegalCommand))),
    ResponseVerb('START', 'STA', (
        VerbResponse(ifNotHere=True, message="I DON'T SEE THAT HERE.", result=Response.IllegalCommand),
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T START THAT.", result=Response.IllegalCommand))),
    ResponseVerb('BREAK', 'BRE', (
        VerbResponse(ifNoObjectResponse=True, message="I'M TRYING TO BREAK IT, BUT I CAN'T.", result=Response.IllegalCommand))),
    ResponseVerb('CUT', 'CUT', VerbResponse(ifNoObjectResponse=True, message="I'M TRYING. IT DOESN'T WORK.", result=Response.IllegalCommand)),
    ResponseVerb('THROW', 'THR', (
        VerbResponse(ifNotHas=True, message="I CAN'T THROW THAT.", result=Response.IllegalCommand),
        VerbResponse(ifNoObjectResponse =True, message="I CAN'T THROW THAT.", result=Response.IllegalCommand))),
    ResponseVerb('CONNECT', 'CON', (
        VerbResponse(ifNotHere=True, message="I CAN'T CONNECT THAT.", result=Response.IllegalCommand),
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T CONNECT THAT.", result=Response.IllegalCommand))),
    ResponseVerb('BOND-007-', 'BON', (
        VerbResponse(ifAtLocation='CAFETERIA', goTo='BASEMENT', message="WHOOPS! A TRAP DOOR OPENED UNDERNEATH ME AND\nI FIND MYSELF FALLING.\n"),
        VerbResponse(message="NOTHING HAPPENED.", result=Response.IllegalCommand)),
        targetOptional=True))

verbs = BuiltInVerbs(customVerbs)
push = verbs['PUSH'].MakeResponse
pull = verbs['PULL'].MakeResponse
go = verbs['GO'].MakeResponse
get = verbs['GET'].MakeResponse
insert = verbs['INSERT'].MakeResponse
open = verbs['OPEN'].MakeResponse
drop = verbs['DROP'].MakeResponse
wear = verbs['WEAR'].MakeResponse
read = verbs['READ'].MakeResponse
start = verbs['START'].MakeResponse
break_ = verbs['BREAK'].MakeResponse
cut = verbs['CUT'].MakeResponse
throw = verbs['THROW'].MakeResponse
connect = verbs['CONNECT'].MakeResponse
look = verbs['LOOK'].MakeResponse