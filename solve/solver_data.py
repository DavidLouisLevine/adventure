class SolverData:
    def __init__(self):
        self.items = {}
        self['GAMMA'] = (0.5, "discounted factor")
        self['TRAINING_EP'] = (0.5, "nominal value of epsilon-greedy parameter for training")
        self['TRAINING_EP_MIN'] = (0.5, "minimum value of epsilon-greedy parameter for training")
        self['TRAINING_EP_MAX'] = (0.5, "maximum value of epsilon-greedy parameter for training")
        self['TESTING_EP'] = (0.05, "epsilon-greedy parameter for testing")
        self['NUM_RUNS'] = 1
        self['NUM_EPOCHS'] = 200
        self['NUM_EPIS_TRAIN'] = (25, "number of episodes for training at each epoch")
        self['NUM_EPIS_TEST'] = (50, "number of episodes for testing")
        self['MAX_PASSES_FITTED_Q'] = (0, "number of passes of the fitted q supervised learning set")
        self['LOSS_TOLERANCE_FITTED_Q'] = (0, "ratio delta average loss between passes divided by average loss, which terminates learning")
        self['EPOCH_TIME_RATIO_FITTED_Q'] = (0.8, "desired ratio between epoch time and fitted q time, which epoch time adjusts to satisfy")
        self['LEARN_WHILE_TRAINING'] = (True, "whether training passes update q values, typically True unless MAX_PASSES_FITTED_Q != 0")
        self['MAX_STEPS'] = (20, "maxiumum number of steps in an espisode")
        self['ALPHA'] = (0.1, "learning rate for training")
        self['HIDDEN_SIZE'] = (200, "number of nodes in the hidden layer of a one-level dqn")
        self['REPEATED_STATE_PENALTY'] = (-0.2, "subtract from reward when the state repeats")
        self['PRINT_LOG_THRESHOLD'] = (10, "Set this lower to print the activity once the ewma reward hits a threshold")

    # Value is a tuple (actualValue, explanationStr)
    # If value isn't a tuple then it is
    # actualValue. In that case, if key exists then
    # update value and keep the existing explanationStr
    def __setitem__(self, key, value):
        if type(value) is not tuple:
            if key in self.items:
                self.items[key] = (value, self.GetItemExplanation(key))
            else:
                self.items[key] = (value, None)
        else:
            self.items[key] = value

    def __getitem__(self, item):
        return self.items[item][0]

    def __iter__(self):
        for item in self.items:
            yield item

    def GetItemExplanation(self, key):
        if key in self.items:
            return self.items[key][1]
        else:
            return ""

    def __str__(self):
        s = ""
        for key in self.items.keys():
            if s != "":
                s += " "
            s += key + '=' + str(self[key])
        return s