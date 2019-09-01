from state import State

class Response:
    def __init__(self, iVerb, f, *args, **kwargs):
        self.iVerb = iVerb
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.travelTo = None
        self.isFatal = False

    def Arg(self, arg):
        return None if arg not in self.kwargs else self.kwargs[arg]

    def ArgStr(self, arg):
        return "" if self.Arg(arg) is None else self.Arg(arg)

    @staticmethod
    def Respond(responses, iVerb, game):
        if type(responses) is Response:
            responses = (responses,)
        for response in responses:
            if response.iVerb == iVerb:
                if response.Arg('condition') is None or response.Arg('condition')(game):
                    m = ""
                    if response.Arg('travelTo') is not None:
                        game.TravelTo(response.ArgStr('travelTo'))
                    if response.Arg('setState') is not None:
                        setStates = response.Arg('setState')
                        if type (setStates[0]) is not tuple:
                            setStates = (setStates, )
                        for setState in setStates:
                            game.state[setState[0]] = setState[1]
                    if response.Arg('createHere') is not None:
                        game.CreateHere(response.Arg('createHere'))
                    if response.Arg('removeObject') is not None:
                        game.world.RemoveObject(response.Arg('removeObject'))
                    if response.Arg('replaceObject') is not None:
                        game.world.RemoveObject(response.Arg('replaceObject')[0])
                        game.CreateHere(response.Arg('replaceObject')[1])
                    if response.isFatal == True:
                        game.state.isDead = True
                        game.quitting = True
                    m += response.ArgStr('message')
                    if response.f is not None:
                        if m != "":
                            m += '\n'
                        m += response.f(game, response.args, response.kwargs)
                    return m

    @staticmethod
    def GetResponse(responses, iVerb):
        if type(responses) is Response:
            responses = (responses,)
        for response in responses:
            if response.iVerb == iVerb:
                return response

        return None

    @staticmethod
    def HasResponse(responses, iVerb):
        return Response.GetResponse(responses, iVerb) is not None
