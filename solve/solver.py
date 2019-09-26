"""Solve an adventure game"""

# Parts of this file are marked private because they contain university course student homework content
# PM this project to get access

import torch
import numpy as np
from tqdm import tqdm
import solve.framework as framework
import solve.utils as utils
from solve.solver_data import SolverData
from pynput import keyboard

DEBUG = False
MAX_CHOOSE_TRIES = 1

log_training = False
log_testing = False

best_reward = None

def ToggleLog(k):
    global log_training, log_testing
    if hasattr(k, 'name'):
        if k.name == "f2":
            log_training = not log_training
        if k.name == "f3":
            log_testing = not log_testing

def DoNothing(_):
    pass

class Solver():
    def __init__(self, framework, predictor, solverData=None, strategy=None):
        self.framework = framework
        self.predictor = predictor
        self.strategy = strategy
        self.best_reward = None
        self.longest_progress = 1    # Greatest number of moves without an entirely negative tail

        if solverData is None:
            self.solverData = SolverData()
        else:
            self.solverData = solverData

        print("\n")  # try to avoid being on the same line as the initial tqdm banner
        print(self.solverData)
        print("")  # try to avoid being on the same line as the initial tqdm banner

        self.dictionary = utils.bag_of_words(self.strategy.get_descriptions())
        self.state_dim = len(self.dictionary)
        self.predictor.Init(self.solverData, framework.num_actions, framework.num_objects, self.state_dim)

        self.listener = keyboard.Listener(
            on_press=ToggleLog,
            on_release=DoNothing)

        self.listener.start()

    def epsilon_greedy(self, state_vector, epsilon):
        """Returns an action selected by an epsilon-greedy exploration policy

        Args:
            state_vector (torch.FloatTensor): extracted vector representation
            epsilon (float): the probability of choosing a random command

        Returns:
            (int, int, bool, tensor): the indices describing the action/object to take
                the bool is True is they were selected (not random), and q is the corresponding
                predicted reward
        """
        # TODO Your code here
        return action_index, object_index, selected, q

    # Return action_index, object_index
    def choose_action(self, state_vector, epsilon):
        i = 0
        while i < MAX_CHOOSE_TRIES:
            action_index, object_index, selected, q = self.epsilon_greedy(state_vector, epsilon)
            if MAX_CHOOSE_TRIES == 1 or self.strategy.move_allowed(int(action_index), int(object_index)):
                break
            i += 1
        return action_index, object_index, selected, q

    def learn(self, current_state_vector, action_index, object_index, reward, next_state_vector, terminal,
              solverData):
        """Updates the weights of the DQN for a given transition

        Args:
            current_state_vector (torch.FloatTensor): vector representation of current state
            action_index (int): index of the current action
            object_index (int): index of the current object
            reward (float): the immediate reward the agent recieves from playing current command
            next_state_vector (torch.FloatTensor): vector representation of next state
            terminal (bool): True if this epsiode is over

        Returns:
            None
        """
        _, _, maxq_next = self.predictor.q_max(next_state_vector, no_grad=True)

        current = self.predictor.q(current_state_vector, action_index, object_index)

        # TODO Your code here

        self.predictor.backward(loss, action_index, object_index)

    def get_epsilon(self, for_training, t):
        if for_training:
            if t >= self.longest_progress:
                epsilon = utils.linear_interpolate((self.longest_progress, self.solverData['TRAINING_EP']), (
                self.solverData['MAX_STEPS'] - 1, self.solverData['TRAINING_EP_MAX']), t)
            else:
                epsilon = utils.linear_interpolate((0, self.solverData['TRAINING_EP_MIN']),
                                                   (self.longest_progress, self.solverData['TRAINING_EP']), t)
        else:
            epsilon = self.solverData['TESTING_EP']
        return epsilon

    def state_vector_from_state(self, state):
        return torch.FloatTensor(utils.extract_bow_feature_vector(state, self.dictionary))

    def run_episode(self, for_training):
        global log_training, log_testing
        """
            Runs one episode
            If for training, update Q function
            If for testing, computes and return cumulative discounted reward
        """
        global best_reward
        epsilon = self.solverData['TRAINING_EP'] if for_training else self.solverData['TESTING_EP']
        epi_reward = 0

        commands = []
        states = {}
        current_state = None

        # initialize for each episode
        t = 0
        all_positive = True
        (current_room_desc, current_quest_desc, terminal) = self.framework.new_game(self.solverData['MAX_STEPS'])
        while not terminal:
            epsilon = self.get_epsilon(for_training, t)

            # Choose next action and execute
            if current_state is None:
                current_state = self.strategy.get_state(current_room_desc)
            current_state_vector = self.state_vector_from_state(current_state)

            # TODO Your code here

            # update reward
            current_state = self.strategy.get_state(current_room_desc)

            if next_state in states:
                reward += self.solverData['ALREADY_SEEN_PENALTY']
            else:
                states[next_state] = ""

            epi_reward += reward * self.solverData['GAMMA'] ** t

            commands += [self.framework.get_action_name(action_index) + ' ' + self.framework.get_object_name(object_index)]
            if reward >= self.framework.get_success_reward() and all_positive:
                if t > self.longest_progress:
                    print(epi_reward, ', *', self.longest_progress, ':', '->'.join(commands), 'training' if for_training else 'testing')
                    self.longest_progress = t
            else:
                all_positive = False

            if for_training:
                # update Q-function.
                # TODO Your code here

            self.log(for_training, log_training, log_testing, action_index, object_index, reward, current_state, current_state_vector, current_quest_desc, next_state_vector, next_room_desc, terminal, epsilon)

            # prepare next step
            # TODO Your code here
            t += 1

        if (self.best_reward is None or epi_reward > self.best_reward) and not for_training:
            print(epi_reward, ', ', self.longest_progress, ':', '->'.join(commands), 'training' if for_training else 'testing')
            self.best_reward = epi_reward

        if not for_training:
            return epi_reward

    def run_epoch(self):
        global log_training, log_testing
        """Runs one epoch and returns reward averaged over test episodes"""
        rewards = []
        self.framework.new_epoch()

        for n in range(self.solverData['NUM_EPIS_TRAIN']):
            if log_training:
                print("TRAIN EPISODE", n)
            self.run_episode(for_training=True)

        for n in range(self.solverData['NUM_EPIS_TEST']):
            if log_testing:
                print("TEST EPISODE", n)
            rewards.append(self.run_episode(for_training=False))

        return np.mean(np.array(rewards))

    def run(self):
        global log_testing
        """Returns array of test reward per epoch for one run"""
        best_ewma_reward = None

        single_run_epoch_rewards_test = []
        pbar = tqdm(range(self.solverData['NUM_EPOCHS']), ncols=80)
        for _ in pbar:
            single_run_epoch_rewards_test.append(self.run_epoch())
            avg_reward = np.mean(single_run_epoch_rewards_test)
            ewma_reward = utils.ewma(single_run_epoch_rewards_test)
            if best_ewma_reward is None or ewma_reward > best_ewma_reward:
                best_ewma_reward = ewma_reward
            if ewma_reward > self.solverData['PRINT_LOG_THRESHOLD']:
                log_testing = True
            pbar.set_description(
                "Avg reward: {:0.6f} | Ewma reward: {:0.6f} | Best Ewma reward: {:0.6f}".format(avg_reward, ewma_reward, best_ewma_reward))
        return single_run_epoch_rewards_test

    def execute(self):
        epoch_rewards_test = []  # shape NUM_RUNS * NUM_EPOCHS

        for _ in range(self.solverData['NUM_RUNS']):
            epoch_rewards_test.append(self.run())
        return epoch_rewards_test

    def log(self, for_training, log_training, log_testing, action_index, object_index, reward, current_state, current_state_vector, current_quest_desc, next_state_vector, next_room_desc, terminal, epsilon):
        if for_training:
            if log_training:
                print('training:', self.framework.get_action_name(action_index),
                      self.framework.get_object_name(object_index), epsilon, ':', current_state, '->', next_room_desc,
                      current_quest_desc, reward)
        if not for_training:
            if log_testing:
                print('testing:', self.framework.get_action_name(action_index),
                      self.framework.get_object_name(object_index), epsilon, ':', current_state, '->', next_room_desc,
                      current_quest_desc, reward)
