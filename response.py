class Response:
    def __init__(self, verb, f, *args, **kwargs):
        self.verb = verb
        self.f = f
        self.args = args
        self.kwargs = kwargs

    @staticmethod
    def Respond(responses, world):
        if type(responses) is Response:
            responses = (responses,)
        for response in responses:
            if response.f is not None:
                if 'condition' not in response.kwargs or response.kwargs['condition'](world):
                    return response.f(world, response.args, response.kwargs)