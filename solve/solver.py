"""Solve an adventure game"""

# Parts of this file are marked private because they contain university course student homework content
# PM this project to get access

import torch
import numpy as np
from tqdm import tqdm
import solve.framework as framework
import solve.utils as utils
from datetime import datetime
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
        if k.name == "f7":
            log_training = not log_training
        if k.name == "f8":
            log_testing = not log_testing

def DoNothing(_):
    pass

class Solver():
    def __init__(self, framework, predictor, solverData=None, strategy=None):
        if solverData is None:
            self.solverData = SolverData()
        else:
            self.solverData = solverData

        self.framework = framework
        self.predictor = predictor
        self.strategy = strategy
        self.best_reward = None
        self.longest_progress = 1    # Greatest number of moves without an entirely negative tail
        self.experiences = set()
        self.experience_tries = 0
        self.num_epis_train = self.solverData['NUM_EPIS_TRAIN']
        self.ascii = True # Controls the tqdm ascii property
        self.previous_fitted_q_count = self.solverData['MAX_PASSES_FITTED_Q']
        self.longest_progress_str = ''
        self.inner_pbar_leave = False
        self.pbar_ncols = 250

        #print("\n")  # try to avoid being on the same line as the initial tqdm banner
        #print(self.solverData)
        #print("")  # try to avoid being on the same line as the initial tqdm banner

        self.dictionary = utils.bag_of_words(self.strategy.get_descriptions())
        self.state_dim = len(self.dictionary)
        self.predictor.Init(self.solverData, self.framework.num_actions, self.framework.num_objects, self.state_dim)

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

    def get_target_q(self, qmax_next, reward, gamma, terminal):
        # TODO Your code here

    def learn_with_target_q(self, current_state_vector, action_index, object_index, target_q):
        """Updates the weights of the DQN for a given transition

        Args:
            current_state_vector (torch.FloatTensor): vector representation of current state
            action_index (int): index of the current action
            object_index (int): index of the current object
            target_q (tensor): expected q value after taking the specified action

        Returns:
            None
        """
        current_q = self.predictor.q(current_state_vector, action_index, object_index)

        # Calculate the loss
        # TODO Your code here

        self.predictor.backward(loss, action_index, object_index)
        return float(loss)

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
        _, _, qmax_next = self.predictor.q_max(next_state_vector, no_grad=True)
        target_q = self.get_target_q(qmax_next, reward, solverData['GAMMA'], terminal)

        self.learn_with_target_q(current_state_vector, action_index, object_index, target_q)

    def get_epsilon(self, for_training, t):
        """Get epsilon, adjusted for the current step count"""
        if for_training:
            if t >= self.longest_progress:
                epsilon = utils.linear_interpolate((self.longest_progress, self.solverData['TRAINING_EP']), (
                self.solverData['MAX_STEPS'], self.solverData['TRAINING_EP_MAX']), t)
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

        experiences = set()

        # initialize for each episode
        t = 0
        all_positive = True
        (current_room_desc, current_quest_desc, terminal) = self.framework.new_game(self.solverData['MAX_STEPS'])
        n = 1
        while not terminal:
            epsilon = self.get_epsilon(for_training, t)

            # Choose next action and execute
            current_state = self.strategy.get_state(current_room_desc)
            current_state_vector = self.state_vector_from_state(current_state)

            # TODO Your code here

            # update reward
            if next_state in states:
                reward += self.solverData['REPEATED_STATE_PENALTY']
            else:
                states[next_state] = ""

            epi_reward += reward * self.solverData['GAMMA'] ** t

            commands += [self.framework.get_action_name(action_index) + ' ' + self.framework.get_object_name(object_index)]
            if reward >= self.framework.get_success_reward() and all_positive:
                if t > self.longest_progress:
                    self.longest_progress_str = '{:2d}: {} {}'.format(self.longest_progress, '->'.join(commands), 'training' if for_training else 'testing')
                    #print(epi_reward, ', *', longest_progress_str)
                    self.longest_progress = t
            else:
                all_positive = False

            if for_training and self.solverData['LEARN_WHILE_TRAINING']:
                # update Q-function.
                # TODO Your code here

            self.log(for_training, log_training, log_testing, action_index, object_index, reward, current_state, current_state_vector, current_quest_desc, next_state_vector, next_room_desc, terminal, epsilon)

            # prepare next step
            # TODO Your code here

            self.experience_tries += 1
            self.experiences.add(Solver.Experience(current_state_vector, action_index, object_index, reward, next_state_vector, terminal))
            t += 1

        if (self.best_reward is None or epi_reward > self.best_reward) and not for_training:
            #print(epi_reward, ', ', self.longest_progress, ':', '->'.join(commands), 'training' if for_training else 'testing')
            self.best_reward = epi_reward

        if not for_training:
            return epi_reward

    def format_seen_ratio(self, seen, count, total):
        if not seen:
            return ' X '
        elif count == 0:
            return ' ' * 3
        else:
            return '{:2d}'.format(int(100 * count / total)) + '%'

    def update_episode_status(self, n):
        for location in self.framework.game.world.locations:
            self.seen_location_count[location.i] += 1 if location.seen else 0
        for object in self.framework.game.world.objects:
            self.seen_object_count[object.i] += 1 if object.seen else 0
        iDoor = self.framework.game.world.objects['AN OPEN WOODEN DOOR'].i
        self.episode_status_str = ' '.join(
            map(lambda x: self.framework.game.world.locations[x].abbreviation + ' ' + \
                          self.format_seen_ratio(framework.seen_locations[x], self.seen_location_count[x], n), \
                range(len(self.framework.game.world.locations)))) + ' OPEN DOOR ' + \
            self.format_seen_ratio(framework.seen_objects[iDoor], self.seen_location_count[iDoor], n)

    def update_inner_pbar(self, pbar, name, format, *args):
        pbar.display(("{:24s} " + format).format(name, *args)[:250])

    def run_epoch(self):
        global log_training, log_testing
        """Runs one epoch and returns reward averaged over test episodes"""
        rewards = []
        self.framework.new_epoch()
        self.seen_location_count = [0] * len(self.framework.game.world.locations)
        self.seen_object_count = [0] * len(self.framework.game.world.objects)

        datetime0 = datetime.now()
        pbar = tqdm(range(self.num_epis_train), ncols=self.pbar_ncols, ascii=self.ascii, leave=self.inner_pbar_leave)
        n = 1
        for _ in pbar:
            n += 1
            self.update_episode_status(n)
            self.update_inner_pbar(pbar, 'TRAIN EPISODE', '{:4d}/{:4d} {} {}', n, self.num_epis_train, self.episode_status_str, self.longest_progress_str)
            if log_training:
                print("TRAIN EPISODE", n)
            self.run_episode(for_training=True)
        pbar.close()

        pbar = tqdm(range(self.solverData['NUM_EPIS_TEST']), ncols=self.pbar_ncols, ascii=self.ascii, leave=self.inner_pbar_leave)
        n = 1
        for _ in pbar:
            n += 1
            self.update_inner_pbar(pbar, 'TEST EPISODE', '{:4d}/{:4d} {} {}', n, self.solverData['NUM_EPIS_TEST'], self.episode_status_str,  self.longest_progress_str)
            if log_testing:
                print("TEST EPISODE", n)
            rewards.append(self.run_episode(for_training=False))
        pbar.close()

        epoch_time = datetime.now() - datetime0

        datetime0 = datetime.now()
        self.fitted_q_learning()
        fitted_q_datetime = datetime.now() - datetime0

        # Match the epoch duration to the fitted q duration. We don't want to over-emphasize either one. Set the ratio
        # parameter low enough so that it doesn't drive the fitted q time by prematurely making too many experiences
        self.num_epis_train = int(self.solverData['EPOCH_TIME_RATIO_FITTED_Q'] * self.num_epis_train * fitted_q_datetime / epoch_time)

        # store for debug reporting for now
        self.epoch_secs = epoch_time.total_seconds()
        self.fitted_q_secs = fitted_q_datetime.total_seconds()

        return np.mean(np.array(rewards))

    def fitted_q_learning(self):
        d_sup = set()
        pbar = tqdm(self.experiences, ncols=self.pbar_ncols, ascii=self.ascii, leave=self.inner_pbar_leave)
        n = 0
        for experience in pbar:
            n += 1
            self.update_inner_pbar(pbar, 'Fitted Q accumulate pass', '{:4d}/{:4d} {} {}', n, len(self.experiences), self.episode_status_str,  self.longest_progress_str)
            with torch.no_grad():
                _, _, q_max = self.predictor.q_max(experience.next_state_vector, no_grad=True)
            target_q = self.get_target_q(q_max, experience.reward, self.solverData['GAMMA'], experience.terminal)
            d_sup.add(
                ((experience.current_state_vector, experience.action_index, experience.object_index), target_q))
        pbar.close()

        self.predictor.Init(self.solverData, self.framework.num_actions, self.framework.num_objects, self.state_dim)

        previous_average_loss = None
        average_loss = None
        pbar = tqdm(range(self.solverData['MAX_PASSES_FITTED_Q']), ncols=self.pbar_ncols, ascii=self.ascii, leave=self.inner_pbar_leave)
        n_max = None
        for n in pbar:
            self.update_inner_pbar(pbar, 'Fitted Q learn pass', '{:4d}/{:4d} {} {}', n, self.previous_fitted_q_count, self.episode_status_str,  self.longest_progress_str)
            # break out of pbar loop will leave previous pbar lines
            if previous_average_loss is None or abs(average_loss - previous_average_loss) / utils.avg((average_loss, previous_average_loss)) >= self.solverData['LOSS_TOLERANCE_FITTED_Q']:
                total_loss = 0
                for ((current_state_vector, action_index, object_index), target_q) in d_sup:
                    total_loss += self.learn_with_target_q(current_state_vector, action_index, object_index, target_q)
                previous_average_loss = average_loss
                average_loss = total_loss / self.solverData['MAX_PASSES_FITTED_Q']
            elif n_max is None:
                n_max = n
        pbar.close()

        self.previous_fitted_q_count = n_max

    def run(self):
        global log_testing
        """Returns array of test rewards per epoch for one run"""
        best_ewma_reward = None

        single_run_epoch_rewards_test = []
        pbar = tqdm(range(self.solverData['NUM_EPOCHS']), ncols=80, ascii=self.ascii)
        for _ in pbar:
            single_run_epoch_rewards_test.append(self.run_epoch())
            avg_reward = np.mean(single_run_epoch_rewards_test)
            ewma_reward = utils.ewma(single_run_epoch_rewards_test)
            if best_ewma_reward is None or ewma_reward > best_ewma_reward:
                best_ewma_reward = ewma_reward
            if ewma_reward > self.solverData['PRINT_LOG_THRESHOLD']:
                log_testing = True
            efficiency = len(self.experiences) / self.experience_tries
            pbar.set_description(
                "Avg reward: {:0.6f} | Ewma reward: {:0.6f} | Best Ewma reward: {:0.6f} Efficiency: {:0.3f}/{} E/Q:{:0.2f}/{:0.2f}={}".\
                    format(avg_reward, ewma_reward, best_ewma_reward, efficiency, len(self.experiences), self.epoch_secs, self.fitted_q_secs, self.num_epis_train))
        pbar.close()
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


    class Experience:
        def __init__(self, current_state_vector, action_index, object_index,reward, next_state_vector, terminal):
            self.current_state_vector = current_state_vector
            self.action_index = action_index
            self.object_index = object_index
            self.reward = reward
            self.next_state_vector = next_state_vector
            self.terminal = terminal

        @staticmethod
        def hash_state_vector(state_vector):
            return tuple(map(lambda x: float(x), tuple(state_vector)))

        def __hash__(self):
            result = hash((Solver.Experience.hash_state_vector(self.current_state_vector), self.action_index, self.reward,\
                         Solver.Experience.hash_state_vector(self.next_state_vector), self.terminal))
            return result

        def __eq__(self, other):
            return  self.current_state_vector.equal(other.current_state_vector) and\
                self.action_index == other.action_index and\
                self.object_index == other.object_index and \
                self.reward == other.reward and \
                self.terminal == other.terminal and \
                self.next_state_vector.equal(other.next_state_vector)

        def __ne__(self, other):
            # Not strictly necessary, but to avoid having both x==y and x!=y
            # True at the same time
            return not(self == other)