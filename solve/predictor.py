"""Tabular QL agent"""

class Predictor:
    def q_max(self, state_vector, no_grad=False):
        pass

    def q(self, state_vector, action_index, object_index):
        pass

    def backward(self, loss, action_index, object_index):
        pass
