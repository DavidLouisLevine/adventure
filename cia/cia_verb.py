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
        if target.IsObject() and not target.value.response is None:
            if Response.HasResponse(target.value.response, self.index):
                m = Response.Respond(target.value.response, self.index, game)
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
        if target.IsObject() and not target.value.response is None:
            response = Response.get(target.value.response, self.index);
            if response is not None:
                into = game.objects[game.input("TELL ME, IN ONE WORD, INTO WHAT")]
                if into == response.kwargs['insertedObject']:
                    m = Response.Respond(target.value.response, self.index, game)
                    if m == "" or m is None:
                        m = "NOTHING HAPPENED."
            else:
                m = "I CAN'T INSERT THAT!"
        else:
            m = ""
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
        kwargs['didntWorkMessage'] = 'SHOULD NOT SEE THIS MESSAGE'
        StandardVerb.__init__(self, *args, **kwargs)

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
    (Verb('CUT', 'CUT')),
    (Verb('THROW', 'THR')),
    (Verb('CON', 'CON')),
    (Verb('BOND-007-', 'BON')),)

verbs = BuiltInVerbs(customVerbs)