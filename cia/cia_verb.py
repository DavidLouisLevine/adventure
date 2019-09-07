from adventure.response import Response
from adventure.verb import Verb, BuiltInVerbs

def ArgStr(kwargs, key):
    return kwargs[key] if key in kwargs else ""

class StandardVerb(Verb):
    def __init__(self, *args, **kwargs):
        self.notApplicableMessage = ArgStr(kwargs, 'notApplicableMessage')
        self.didntWorkMessage = ArgStr(kwargs, 'didntWorkMessage')
        if 'notApplicableMessage' in kwargs:
            self.notApplicableMessage = kwargs.pop('notApplicableMessage')
        if 'didntWorkMessage' in kwargs:
            self.didntWorkMessage = kwargs.pop('didntWorkMessage')
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if target.IsObject():
            if Response.HasResponse(target.value.responses, self):
                m = Response.Respond(target.value.responses, self, game)
                if m == "" or m is None:
                    m = self.didntWorkMessage
            else:
                m = self.notApplicableMessage if self.notApplicableMessage is not None else self.didntWorkMessage
        else:
            m = ""
        return m

class PushVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['didntWorkMessage'] = 'NOTHING HAPPENS.'
        StandardVerb.__init__(self, *args, **kwargs)

class PullVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['didntWorkMessage'] = 'NOTHING HAPPENS.'
        StandardVerb.__init__(self, *args, **kwargs)

class InsertVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        if 'didntWorkMessage' not in kwargs:
            kwargs['didntWorkMessage'] = 'NOTHING HAPPENED.'
        StandardVerb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        m = ""
        if target.IsObject() and not target.value.responses is None:
            response = Response.GetResponse(target.value.responses, self);
            if response is not None:
                into = game.world.objects[game.Input("TELL ME, IN ONE WORD, INTO WHAT")]
                if 'insertedObject' in response.kwargs and into == response.kwargs['insertedObject']:
                    m = Response.Respond(target.value.responses, self, game)
                if m == "" or m is None:
                    m = "NOTHING HAPPENED."
            else:
                m = "I CAN'T INSERT THAT!"
        return m

class OpenVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I CAN'T OPEN THAT!"
        kwargs['didntWorkMessage'] = "I CAN'T DO THAT......YET!"
        StandardVerb.__init__(self, *args, **kwargs)

class WearVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I CAN'T WEAR THAT!"
        kwargs['didntWorkMessage'] = 'SHOULD NOT SEE THIS MESSAGE'
        StandardVerb.__init__(self, *args, **kwargs)

class ReadVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I CAN'T READ THAT."
        kwargs['didntWorkMessage'] = 'SHOULD NOT SEE THIS MESSAGE'
        StandardVerb.__init__(self, *args, **kwargs)

class StartVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I CAN'T START THAT."
        kwargs['didntWorkMessage'] = 'SHOULD NOT SEE THIS MESSAGE'
        StandardVerb.__init__(self, *args, **kwargs)

class BreakVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I'M TRYING TO BREAK IT, BUT I CAN'T."
        kwargs['didntWorkMessage'] = "I CAN'T DO THAT YET."
        StandardVerb.__init__(self, *args, **kwargs)

class CutVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I'M TRYING. IT DOESN'T WORK."
        kwargs['didntWorkMessage'] = 'SHOULD NOT SEE THIS MESSAGE'
        StandardVerb.__init__(self, *args, **kwargs)

class ThrowVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I CAN'T THROW THAT."
        kwargs['didntWorkMessage'] = 'SHOULD NOT SEE THIS MESSAGE'
        StandardVerb.__init__(self, *args, **kwargs)

class ConnectVerb(StandardVerb):
    def __init__(self, *args, **kwargs):
        kwargs['notApplicableMessage'] = "I CAN'T CONNECT THAT."
        kwargs['didntWorkMessage'] = 'SHOULD NOT SEE THIS MESSAGE'
        StandardVerb.__init__(self, *args, **kwargs)

class BondVerb(Verb):
    def __init__(self, *args, **kwargs):
        Verb.__init__(self, *args, **kwargs)

    def DoObject(self, target, game):
        if game.state.location != game.world.locations['CAFETERIA']:
            return "NOTHING HAPPENED."
        else:
            game.state.location = game.world.locations['BASEMENT']
            return "WHOOPS! A TRAP DOOR OPENED UNDERNEATH ME AND\nI FIND MYSELF FALLING.\n"

customVerbs = (
    (PushVerb('PUSH', 'PUS')),
    (PullVerb('PULL', 'PUL')),
    (InsertVerb('INSERT', 'INS')),
    (OpenVerb('OPEN', 'OPE')),
    (WearVerb('WEAR', 'WEA')),
    #(WearVerb('WEAR', 'WEA', targetInventory=False, targetInRoom=False)),
    (ReadVerb('READ', 'REA')),
    (StartVerb('START', 'STA')),
    (BreakVerb('BREAK', 'BRE')),
    (CutVerb('CUT', 'CUT')),
    (ThrowVerb('THROW', 'THR')),
    (ConnectVerb('CON', 'CON', targetInventory=False, targetInRoom=False)),
    (BondVerb('BOND-007-', 'BON', targetOptional=True)),)

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