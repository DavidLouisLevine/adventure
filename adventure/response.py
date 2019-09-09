from adventure.util import MakeTuple
from adventure.direction import Direction

class Response:
    def __init__(self, verb, f, *args, **kwargs):
        self.verb = verb
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.goTo = None
        self.isFatal = False

    def Arg(self, arg):
        return None if arg not in self.kwargs else self.kwargs[arg]

    def ArgStr(self, arg):
        return "" if self.Arg(arg) is None else self.Arg(arg)

    # If the response arg is None then use object
    def IfCondition(self, name, game, condition, object=None):
        arg = self.Arg(name)
        if arg is True:
            if object is not None:
                return condition(object, game)
            else:
                return True
        if arg is not None:
            arg = MakeTuple(arg)
            for a in arg:
                if not condition(a, game):
                    return False
        return True

    @staticmethod
    def ProcessMessage(message, game):
        while '{' in message:
            assert '}' in message
            l = message.index('{')
            r = message.index('}')
            key = message[l + 1:r]
            value = game.state[key]
            message = message[:l] + str(value) + message[r + 1:]
        return message

    def IfQuestion(self, game):
        if 'question' not in self.kwargs:
            return True
        question = self.kwargs['question']
        assert 'answer' in self.kwargs
        expectedAnswer = self.kwargs['answer']
        actualAnswer = game.Input(question, readExpected=False)[0]
        return expectedAnswer == actualAnswer

    def IfObjectResponse(self, verb, object):
        if object is None or self.Arg('ifObjectResponse') is None:
            return True

        return Response.HasResponse(object.responses, verb)

    def IfNoObjectResponse(self, verb, object):
        if object is None or self.Arg('ifNoObjectResponse') is None:
            return True

        return not Response.HasResponse(object.responses, verb)

    @staticmethod
    def Respond(responses, verb, game, object=None):
        responses = MakeTuple(responses)

        for response in responses:
            if response.verb == verb:
                if response.IfObjectResponse(verb, object) and\
                    response.IfNoObjectResponse(verb, object) and\
                    response.IfCondition('ifTrue', game, lambda a, g: a(g), object) and \
                    response.IfCondition('ifSet', game, lambda a, g: g.state[a], object) and\
                    response.IfCondition('ifNotSet', game, lambda a, g: not g.state[a], object) and \
                    response.IfCondition('ifGE', game, lambda a, g: g.state[a] >= 0, object) and \
                    response.IfCondition('ifAtLocation', game, lambda a, g: g.AtLocation(a), object) and \
                    response.IfCondition('ifNotAtLocation', game, lambda a, g: not g.AtLocation(a), object) and \
                    response.IfCondition('ifExists', game, lambda a, g: g.Exists(a), object) and \
                    response.IfCondition('ifHere', game, lambda a, g: g.IsHere(a), object) and \
                    response.IfCondition('ifNotHere', game, lambda a, g: not g.IsHere(a), object) and \
                    response.IfCondition('ifHas', game, lambda a, g: g.Has(a), object) and \
                    response.IfCondition('ifNotHas', game, lambda a, g: not g.Has(a), object) and\
                    response.IfQuestion(game):

                    m = ""

                    if response.Arg('goTo') is not None:
                        game.GoTo(response.ArgStr('goTo'))

                    if response.Arg('setState') is not None:
                        setStates = response.Arg('setState')
                        if type (setStates[0]) is not tuple:
                            setStates = (setStates, )
                        for setState in setStates:
                            game.state[setState[0]] = setState[1]

                    if response.Arg('setMove') is not None:
                        changes = response.Arg('setMove')
                        changes = MakeTuple(changes, 1)
                        for change in changes:
                            location = game.world.locations[change[0]]
                            location.moves[Direction.FromName(change[1]).d] = change[2]

                    if response.Arg('createHere') is not None:
                        for object in MakeTuple(response.Arg('createHere')):
                            game.CreateHere(object)

                    if response.Arg('removeObject') is not None:
                        for object in MakeTuple(response.Arg('removeObject')):
                            game.world.RemoveObject(object)

                    if response.Arg('replaceObject') is not None:
                        for old, new in MakeTuple(response.Arg('replaceObject'), 1):
                            game.ReplaceObject(old, new)

                    if response.Arg('makeVisible') is not None:
                        for object in MakeTuple(response.Arg('makeVisible')):
                            game.world.objects[object].visible = True

                    if response.isFatal == True:
                        game.state.isDead = True
                        game.quitting = True

                    # TODO: Implement replacement strings
                    m += Response.ProcessMessage(response.ArgStr('message'), game)

                    if response.f is not None:
                        if m != "":
                            m += '\n'
                        m_new = response.f(game, response.args, response.kwargs)
                        if m_new is not None:
                            m += m_new

                    if response.Arg('look') is not None:
                        if m != "":
                            m += '\n'
                        m += game.Look(response.ArgStr('look'))

                    return m

    @staticmethod
    def GetResponse(responses, verb):
        if type(responses) is Response:
            responses = (responses,)
        for response in responses:
            if response.verb == verb:
                return response

        return None

    @staticmethod
    def HasResponse(responses, verb):
        if responses is None:
            return False

        return Response.GetResponse(responses, verb) is not None
