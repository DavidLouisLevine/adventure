import torch.nn as nn
import torch.nn.functional as F

class DQN(nn.Module):
    """A deep Q network that maps an input to multiple outputs
    Computes Q values for each (action, object) tuple given an input state vector

    output_dims is a list of output dimensions. There will be one model (and corresponding output)
    for each member of this list.
    """

    def __init__(self, input_dim, output_dims, hidden_size=200):
        super(DQN, self).__init__()
        self.state_encoder = nn.Linear(input_dim, hidden_size)
        self.state2output = list(map(lambda x: nn.Linear(hidden_size, x), output_dims))

    def forward(self, x):
        state = F.relu(self.state_encoder(x))
        return tuple(map(lambda m: m(state), self.state2output))


class DQNStacked(nn.Module):
    """A deep Q network that maps an input to multiple outputs
    Computes Q values for each (action, object) tuple given an input state vector
    """

    def __init__(self, input_dim, output_dim, hidden_size1=200, hidden_size2=200):
        super(DQN, self).__init__()
        self.state_encoder = nn.Linear(input_dim, hidden_size1)
        self.state2output = list(map(lambda x: nn.Linear(hidden_size1, x), output_dim))

        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_size1),
            nn.ReLU(),
            nn.Linear(hidden_size1, hidden_size2),
            nn.ReLU(),
            nn.Linear(hidden_size2, output_dim)
        )


    def forward(self, x):
        return self.model(x)
