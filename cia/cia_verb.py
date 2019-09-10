from adventure.response import Response
from adventure.verb import Verb, BuiltInVerbs
from adventure.util import MakeTuple

class ResponseVerb(Verb):
    def __init__(self, name, abbreviation, responses=None, *args, **kwargs):
        if responses is not None:
            self.responses = MakeTuple(responses)
            for response in self.responses:
                response.verb = self
        else:
            self.responses = None
        if 'notApplicableMessage' in kwargs:
            self.notApplicableMessage = kwargs.pop('notApplicableMessage')
        else:
            self.notApplicableMessage = None
        if 'didntWorkMessage' in kwargs:
            self.didntWorkMessage = kwargs.pop('didntWorkMessage')
        else:
            self.didntWorkMessage = None
        Verb.__init__(self, name, abbreviation, *args, **kwargs)

    def DoObject(self, target, game):
        m = ""
        if Response.HasResponse(self.responses, self):
            m = Response.Respond(self.responses, self, game, target.value if target is not None and target.IsObject() else None)
            if m is not None and m != "":
                return m, 0

        if target.IsObject() and Response.HasResponse(target.value.responses, self):
            m = Response.Respond(target.value.responses, self, game)
            if m is None or m == "":
                m = self.didntWorkMessage
        elif self.notApplicableMessage is not None:
            m = self.notApplicableMessage
        return m, 0

def VerbResponse(*args, **kwargs):
    return Response(None, None, *args, **kwargs)

customVerbs = (
    ResponseVerb('PUSH', 'PUS', (
        VerbResponse(ifNotHere=True, message="I DON'T SEE THAT HERE."),
        VerbResponse(ifNoObjectResponse=True, message="NOTHING HAPPENS."))),
    ResponseVerb('PULL', 'PUL', VerbResponse(ifNoObjectResponse=True, message="NOTHING HAPPENS.")),
    ResponseVerb('INSERT', 'INS',
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T INSERT THAT!"),
        didntWorkMessage="NOTHING HAPPENED."),
    ResponseVerb('OPEN', 'OPE', (
        VerbResponse(ifNotHere=True, message="I CAN'T OPEN THAT!"),
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T OPEN THAT!")),
        didntWorkMessage="I CAN'T DO THAT......YET!"),
    ResponseVerb('WEAR', 'WEA', (
        VerbResponse(ifNotHas=True, message="I CAN'T WEAR THAT!"),
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T WEAR THAT!"))),
    ResponseVerb('READ', 'REA', (
        VerbResponse(ifNoObjectResponse=True, message="I CAN'T READ THAT!"),
        VerbResponse(ifNotHere=True, message="I DON'T SEE THAT HERE."))),
    ResponseVerb('START', 'STA', (
        VerbResponse(ifNotHas=True, message="I CAN'T START THAT!"),
        VerbResponse(ifNoObjectResponse=True, message="SHOULD NOT SEE THIS MESSAGE"))),
    ResponseVerb('BREAK', 'BRE', (
        VerbResponse(ifNoObjectResponse=True, message="I'M TRYING TO BREAK IT, BUT I CAN'T."))),
    ResponseVerb('CUT', 'CUT', VerbResponse(ifNotHas=True, message="I'M TRYING. IT DOESN'T WORK.")),
    ResponseVerb('THROW', 'THR', VerbResponse(ifNotHas=True, message="I CAN'T THROW THAT.")),
    ResponseVerb('CON', 'CON', VerbResponse(ifNotHas=True, message="I CAN'T CONNECT THAT.")),
    ResponseVerb('BOND-007-', 'BON', (
        VerbResponse(ifAtLocation='CAFETERIA', goTo='BASEMENT', message="WHOOPS! A TRAP DOOR OPENED UNDERNEATH ME AND\nI FIND MYSELF FALLING.\n"),
        VerbResponse(message="NOTHING HAPPENED.")),
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