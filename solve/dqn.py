import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    """A deep Q network that maps an input to multiple outputs
    Computes Q values for each (action, object) tuple given an input state vector

    output_dims is a list of output dimensions. There will be one model (and corresponding output)
    for each member of this list.
    """

    def __init__(self, input_dim, output_dims, solverData):
        super(DQN, self).__init__()
        hidden_size = solverData['HIDDEN_SIZE']
        self.state_encoder = nn.Linear(input_dim, hidden_size)
        self.state2output = list(map(lambda x: nn.Linear(hidden_size, x), output_dims))

    def forward(self, x):
        state = F.relu(self.state_encoder(x))
        return tuple(map(lambda m: m(state), self.state2output))


class DQNStacked(nn.Module):
    """A deep Q network that maps an input to multiple outputs
    Computes Q values for each (action, object) tuple given an input state vector
    """

    def __init__(self, input_dim, output_dims, solverData):
        super(DQNStacked, self).__init__()
        hidden_size1 = solverData['HIDDEN_SIZE1']
        hidden_size2 = solverData['HIDDEN_SIZE2']
        self.state2output = list(map(lambda x: nn.Linear(hidden_size2, x), output_dims))

        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_size1),
            nn.ReLU(),
            nn.Linear(hidden_size1, hidden_size2),
            nn.ReLU(),
        )

    def forward(self, x):
        head = self.model(x)
        return tuple(map(lambda m: m(head), self.state2output))

class LSTM(nn.Module):
    """A deep Q network that maps an input to multiple outputs
    Computes Q values for each (action, object) tuple given an input state vector

    output_dims is a list of output dimensions. There will be one model (and corresponding output)
    for each member of this list.
    """

    def __init__(self, input_dim, output_dims, solverData):
        super(LSTM, self).__init__()
        hidden_size = solverData['HIDDEN_SIZE']
        self.state_encoder = nn.Linear(input_dim, hidden_size)
        self.state2output = list(map(lambda x: nn.Linear(hidden_size, x), output_dims))

    def forward(self, x):
        state = F.relu(self.state_encoder(x))
        return tuple(map(lambda m: m(state), self.state2output))