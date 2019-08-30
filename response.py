class Response:
    def __init__(self, iVerb, f, *args, **kwargs):
        self.iVerb = iVerb
        self.f = f
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def Respond(responses, iVerb, game):
        if type(responses) is Response:
            responses = (responses,)
        for response in responses:
            if response.iVerb == iVerb and response.f is not None:
                if 'condition' not in response.kwargs or response.kwargs['condition'](game):
                    return response.f(game, response.args, response.kwargs)

    @staticmethod
    def HasResponse(responses, iVerb):
        if type(responses) is Response:
            responses = (responses,)
        for response in responses:
            if response.iVerb == iVerb and response.f is not None:
                return True

        return False