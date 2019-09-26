from adventure.util import MakeTuple
from adventure.direction import Direction
from itertools import accumulate

class Response:
    def __init__(self, verb, f, *args, **kwargs):
        self.verb = verb
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.goTo = None
        self.isFatal = False

    # Results
    Success = 0
    QuestCompleted = 1
    IllegalCommand = 2  # eg: READ NORTH
    Fatal = 3           # eg: You're dead
    MaybeLater = 4      # eg: Can't do that yet
    NotUseful = 5       # eg: No TV is connected
    NewlySeen = 6       # eg: Just used for reward lookup
    MightBeUseful = 7   # eg: GET <anything>

    @staticmethod
    def IsSuccessfulResult(result):
        return result in (Response.Success, Response.QuestCompleted)

    def Arg(self, arg, default=None):
        return default if arg not in self.kwargs else self.kwargs[arg]

    def ArgStr(self, arg):
        return "" if self.Arg(arg) is None else self.Arg(arg)

    def HasArg(self, arg):
        return self.Arg(arg) is not None

    # If the response arg is None then use object
    def IfCondition(self, name, game, condition, object=None, accumulator=None):
        arg = self.Arg(name)
        # True is a placeholder for for the current object and is used in verb responses
        if arg is True:
            if object is not None:
                c = condition(object, game)
                if c is False:
                    jj = 99
                return c
            else:
                return True
        if arg is not None:
            if type(arg) is not tuple or accumulator is None:
                c = condition(arg, game)
                if c is False:
                    jj = 99
                return c
            args = MakeTuple(arg)
            return list(accumulate(map(lambda x: condition(x, game), args), accumulator))[-1]
        return True

    def IsConditional(self):
        for arg in self.kwargs:
            if arg[:2] == 'if':
                return True
        return False

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
        expectedAnswer = self.ProcessMessage(expectedAnswer, game)
        actualAnswer = game.Input(question, readExpected=False)[0]
        return expectedAnswer == actualAnswer

    def IfObjectResponse(self, verb, object):
        if object is None or not self.HasArg('ifObjectResponse'):
            return True

        return Response.HasResponse(object.responses, verb)

    def IfNoObjectResponse(self, verb, object):
        if object is None or not self.HasArg('ifNoObjectResponse'):
            return True

        return not Response.HasResponse(object.responses, verb)

    @staticmethod
    def Respond(responses, verb, game, object=None, post=False):
        responses = MakeTuple(responses)
        m = ""
        reward = 0
        result = Response.Success

        for response in responses:
            if response.verb == verb and post == response.Arg('post', False):
                if response.Arg('breakpoint') is not None:
                    jj = 99  # Put a breakpoint here

                if response.IfObjectResponse(verb, object) and \
                    response.IfNoObjectResponse(verb, object) and\
                    response.IfQuestion(game) and\
                    response.IfCondition('ifTrue', game, lambda a, g: a(g), object) and \
                    response.IfCondition('ifSet', game, lambda a, g: g.state[a], object, accumulator=lambda x, y: x and y) and \
                    response.IfCondition('ifNotSet', game, lambda a, g: not g.state[a], object, accumulator=lambda x, y: x or y) and \
                    response.IfCondition('ifEQ', game, lambda a, g: g.state[a[0]] == a[1], object) and \
                    response.IfCondition('ifGE', game, lambda a, g: g.state[a[0]] >= a[1], object) and \
                    response.IfCondition('ifAtLocation', game, lambda a, g: g.AtLocation(a), object, accumulator=lambda x, y: x or y) and \
                    response.IfCondition('ifNotAtLocation', game, lambda a, g: not g.AtLocation(a), object) and \
                    response.IfCondition('ifExists', game, lambda a, g: g.Exists(a), object) and \
                    response.IfCondition('ifNotExists', game, lambda a, g: not g.Exists(a), object, accumulator=lambda x, y: x or y) and \
                    response.IfCondition('ifHere', game, lambda a, g: g.IsHere(a), object) and \
                    response.IfCondition('ifNotHere', game, lambda a, g: not g.IsHere(a), object) and \
                    response.IfCondition('ifHas', game, lambda a, g: g.Has(a), object) and \
                    response.IfCondition('ifNotHas', game, lambda a, g: not g.Has(a), object) and\
                    response.IfCondition('ifObjectAtLocation', game, lambda a, g: g.ObjectAtLocation(a[0], a[1]), object) and\
                    response.IfCondition('ifNotObjectAtLocation', game, lambda a, g: not g.ObjectAtLocation(a[0], a[1]), object):

                    m = ""

                    if response.HasArg('goTo'):
                        game.GoTo(response.ArgStr('goTo'))

                    if response.HasArg('setState'):
                        setStates = response.Arg('setState')
                        if type (setStates[0]) is not tuple:
                            setStates = (setStates, )
                        for setState in setStates:
                            game.state[setState[0]] = setState[1]

                    if response.HasArg('setMove'):
                        changes = response.Arg('setMove')
                        changes = MakeTuple(changes, 1)
                        for change in changes:
                            location = game.world.locations[change[0]]
                            location.moves[Direction.FromName(change[1]).d] = change[2]

                    if response.HasArg('createHere'):
                        for object in MakeTuple(response.Arg('createHere')):
                            game.CreateHere(object)

                    if response.HasArg('createMine'):
                        for object in MakeTuple(response.Arg('createMine')):
                            game.CreateMine(object)

                    if response.HasArg('removeObject'):
                        for object in MakeTuple(response.Arg('removeObject')):
                            game.RemoveObject(object)

                    if response.HasArg('replaceObject'):
                        for old, new in MakeTuple(response.Arg('replaceObject'), 1):
                            game.ReplaceObject(old, new)

                    if response.HasArg('makeVisible'):
                        for object in MakeTuple(response.Arg('makeVisible')):
                            game.world.objects[object].visible = True

                    m += Response.ProcessMessage(response.ArgStr('message'), game)

                    if response.f is not None:
                        if m != "":
                            m += '\n'
                        m_new = response.f(game, response.args, response.kwargs)
                        if m_new is not None:
                            m += m_new

                    if response.HasArg('look'):
                        if m != "":
                            m += '\n'
                        m += game.Look(response.ArgStr('look'))[0]

                    if response.HasArg('result'):
                        result = response.Arg('result')
                        if result == Response.Fatal:
                            game.state.isDead = True
                            game.quitting = True

                    return m, reward, result
        return m, reward, result

    @staticmethod
    def GetResponse(responses, verb):
        if type(responses) is Response:
            responses = (responses,)
        for response in responses:
            if response.verb == verb:
                return response

        return None

    @staticmethod
    def Responses(responses, verb):
        if responses is None:
            return
        if type(responses) is Response:
            responses = (responses,)
        for response in responses:
            if response.verb == verb:
                yield response

    @staticmethod
    def HasResponse(responses, verb):
        if responses is None:
            return False

        return Response.GetResponse(responses, verb) is not None

    def is_conditional_look_response(self):
        return self.IsConditional() and ('result' not in self.kwargs or self.kwargs['result'] == Response.Success)
