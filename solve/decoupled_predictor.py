import torch
import torch.optim as optim
import solve.utils as utils
from solve.dqn import DQN
from solve.predictor import Predictor

# This predictor considers the resultant action and resultant object as separate, uncorrelated outputs

# Parts of this file are marked private because they contain university course student homework content
# PM this project to get access

class DecoupledPredictor(Predictor):
    def __init__(self, hidden_size=200):
        self.hidden_size = hidden_size

    def Init(self, solverData, num_actions, num_objects, state_dim):
        self.num_actions = num_actions
        self.num_objects = num_objects
        self.model = DQN(state_dim, (num_actions, num_objects), self.hidden_size)
        self.optimizer = optim.SGD(self.model.parameters(), lr=solverData['ALPHA'])

    def combined_q(self, q_action, q_object):
        return utils.avg((q_action, q_object))

    def q_max(self, state_vector, no_grad=False):
        # TODO Your code here
        return action_index, object_index, q_max

    def q(self, state_vector, action_index, object_index):
        # TODO Your code here
        return q

    def backward(self, loss, action_index, object_index):
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
