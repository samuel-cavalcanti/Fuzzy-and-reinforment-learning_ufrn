import numpy as np


class Q_learning:

    def __init__(self, max_num_states, max_num_actions, random_func, alpha=0.1, gamma=0.4, epsilon=1, epsilon_min=0.01,
                 epsilon_decay=0.995, n_resets=0):
        self.q_table = self._generateQTable(max_num_states, max_num_actions)

        # self.q_table = np.random.random((max_num_states, max_num_actions)) * 20 - 10
        self.random = random_func
        self._setHyperParameters(alpha, gamma, epsilon, epsilon_min, epsilon_decay, n_resets)

    def _setHyperParameters(self, alpha, gamma, epsilon, epsilon_min, epsilon_decay, n_resets):

        self._alpha = alpha

        self._gamma = gamma

        self._epsilon = epsilon

        self._epsilon_min = epsilon_min

        self._epsilon_decay = epsilon_decay

        self._n_resets = n_resets

    def _generateQTable(self, max_num_states, max_num_actions):
        return np.zeros([max_num_states, max_num_actions])

    def _explorationOrExploitation(self, state):
        if np.random.uniform(0, 1) < self._epsilon:  # 0.01
            action = self.random()
        else:
            action = np.argmax(self.q_table[state])

        return action

    def action(self, state):
        self._current_state = state
        self._current_action = self._explorationOrExploitation(state)
        return self._current_action

    def update(self, next_state, reward, done, info):

        old_value = self.q_table[self._current_state, self._current_action]
        next_max = np.max(self.q_table[next_state])

        new_value = (1 - self._alpha) * old_value + self._alpha * (reward + self._gamma * next_max)
        self.q_table[self._current_state, self._current_action] = new_value

        if done:
            self._updateEpsilon()

    def _updateEpsilon(self):
        if self._epsilon > self._epsilon_min:
            self._epsilon *= self._epsilon_decay

        elif self._n_resets > 0:
            self._epsilon = 0.5
            self._n_resets -= 1

    def load(self, file):
        self.q_table = np.load(file)
        self._epsilon = 0.01

    def save(self, file):
        np.save(file, self.q_table)

    def getEpsilon(self):
        return self._epsilon
