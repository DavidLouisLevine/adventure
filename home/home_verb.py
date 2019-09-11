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
        m, reward, result = "", 0, Response.IllegalCommand
        if Response.HasResponse(self.responses, self):
            m, reward, result = Response.Respond(self.responses, self, game, target.value if target is not None and target.IsObject() else None)
            if m is not None and m != "":
                return m, reward, result

        if target.IsObject() and Response.HasResponse(target.value.responses, self):
            m, reward, result = Response.Respond(target.value.responses, self, game)
            if m is None or m == "":
                m = self.didntWorkMessage
        elif self.notApplicableMessage is not None:
            m = self.notApplicableMessage
        return m, reward, result

def VerbResponse(*args, **kwargs):
    return Response(None, None, *args, **kwargs)

verbs = BuiltInVerbs((
    #ResponseVerb('go', 'go'),
    ResponseVerb('watch', 'watch'),
    ResponseVerb('eat', 'eat'),
    ResponseVerb('sleep', 'sleep'),
    ResponseVerb('exercise', 'exercise'),
), f=('GO',))

go = verbs['GO'].MakeResponse
exercise = verbs['exercise'].MakeResponse
watch = verbs['watch'].MakeResponse
eat = verbs['eat'].MakeResponse
sleep = verbs['sleep'].MakeResponse
