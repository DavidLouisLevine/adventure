import torch
import torch.optim as optim
import numpy as np
import solve.framework as framework
import solve.utils as utils
from solve.dqn import DQN, DQNStacked
from solve.predictor import Predictor

# This predictor considers the resultant action and resultant object as dependent on each other

class ModelPerVerbPredictor(Predictor):
    def __init__(self, dqn):
        self.dqn = dqn

    def Init(self, solverData, num_actions, num_objects, state_dim):
        self.num_actions = num_actions
        self.num_objects = num_objects
        self.models = list(map(lambda x: self.dqn(state_dim, (num_objects, ), solverData), range(num_actions)))
        self.optimizers = list(map(lambda x: optim.SGD(x.parameters(), lr=solverData['ALPHA']), self.models))

    def q_max(self, state_vector, no_grad=False):
        q_output = [None, ] * self.num_actions
        for i in range(self.num_actions):
            if no_grad:
                with torch.no_grad():
                    q_output[i] = self.models[i](state_vector)[0]
            else:
                q_output[i] = self.models[i](state_vector)[0]
        m = list(map(lambda x: torch.max(x), q_output))
        action_index = utils.argmax(m)
        object_index = utils.argmax(q_output[action_index])
        q_max = q_output[action_index][object_index]
        return action_index, object_index, q_max

    def q(self, state_vector, action_index, object_index):
        return self.models[action_index](state_vector)[0][object_index]

    def backward(self, loss, action_index, object_index):
        self.optimizers[action_index].zero_grad()
        loss.backward()
        self.optimizers[action_index].step()

class ModelPerObjectPredictor(Predictor):
    def __init__(self, dqn):
        self.dqn = dqn

    def Init(self, solverData, num_actions, num_objects, state_dim):
        self.num_actions = num_actions
        self.num_objects = num_objects
        self.models = list(map(lambda x: self.dqn(state_dim, (num_actions, ), solverData), range(num_objects)))
        self.optimizers = list(map(lambda x: optim.SGD(x.parameters(), lr=solverData['ALPHA']), self.models))

    def q_max(self, state_vector, no_grad=False):
        q_output = [None, ] * self.num_objects
        for i in range(self.num_objects):
            if no_grad:
                with torch.no_grad():
                    q_output[i] = self.models[i](state_vector)[0]
            else:
                q_output[i] = self.models[i](state_vector)[0]
        m = list(map(lambda x: torch.max(x), q_output))
        object_index = utils.argmax(m)
        action_index = utils.argmax(q_output[object_index])
        q_max = q_output[object_index][action_index]
        return action_index, object_index, q_max

    def q(self, state_vector, action_index, object_index):
        return self.models[object_index](state_vector)[0][action_index]

    def backward(self, loss, action_index, object_index):
        self.optimizers[object_index].zero_grad()
        loss.backward()
        self.optimizers[object_index].step()

class ModelPerActionPredictor(Predictor):
    def __init__(self, dqn):
        self.dqn = dqn

    def NFromActionObject(self, action_index, object_index):
        return action_index * self.num_objects + object_index

    def Init(self, solverData,  num_actions, num_objects, state_dim):
        self.num_actions = num_actions
        self.num_objects = num_objects
        self.num_models = num_actions * num_objects
        self.models = list(map(lambda x: self.dqn(state_dim, (1, ), solverData), range(self.num_models)))
        self.optimizers = list(map(lambda x: optim.SGD(x.parameters(), lr=solverData['ALPHA']), self.models))

    def q_max(self, state_vector, no_grad=False):
        q_output = [None, ] * self.num_models
        for i in range(self.num_models):
            if no_grad:
                with torch.no_grad():
                    q_output[i] = self.models[i](state_vector)[0]
            else:
                q_output[i] = self.models[i](state_vector)[0]
        n = utils.argmax(q_output)
        action_index = n // self.num_objects
        object_index = n - action_index * self.num_objects
        q_max = q_output[n]
        return action_index, object_index, q_max

    def q(self, state_vector, action_index, object_index):
        return self.models[self.NFromActionObject(action_index, object_index)](state_vector)[0]

    def backward(self, loss, action_index, object_index):
        self.optimizers[self.NFromActionObject(action_index, object_index)].zero_grad()
        loss.backward()
        self.optimizers[self.NFromActionObject(action_index, object_index)].step()

