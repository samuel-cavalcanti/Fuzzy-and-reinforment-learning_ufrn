from .Qlearning import Q_learning
import numpy as np
from collections import deque
import random


class DeepQLearning(Q_learning):
    # reference https://keon.io/deep-q-learning/
    # default values of Q-learning
    # _alpha = 0.1
    # _gamma = 0.4
    # _epsilon = 1
    # _epsilon_min = 0.01
    # _epsilon_decay = 0.995

    def __init__(self, model, random_func, batch_size=64, size_memory=100000, alpha=0.1, gamma=0.99,
                 epsilon=1, epsilon_min=0.01, epsilon_decay=0.995, n_resets=0):

        self._model = model

        self.random = random_func

        self._batch_size = batch_size

        self._maxReward = 0

        if size_memory is not None:
            self._memory = deque(maxlen=size_memory)

        super()._setHyperParameters(alpha, gamma, epsilon, epsilon_min, epsilon_decay, n_resets)

    def _remember(self, current_state, action, reward, next_state, done):
        self._memory.append((current_state, action, reward, next_state, done))

    def _explorationOrExploitation(self, state):

        if np.random.uniform(0, 1) < self._epsilon:
            action = self.random()
        else:
            predict = self._model.predict(state)
            action = np.argmax(predict)

        return action

    def update(self, next_state, reward, done, info):

        if hasattr(self, "_memory"):
            self._remember(self._current_state, self._current_action, reward, next_state, done)
            self._maxReward = reward
            if len(self._memory) > self._batch_size:
                self._replay()
        else:
            self._fitModel(self._current_state, self._current_action, reward, next_state, done)

        if done:
            self._updateEpsilon()

    # https://web.stanford.edu/class/psych209/Readings/MnihEtAlHassibis15NatureControlDeepRL.pdf
    def _replay(self):
        mini_batch = random.sample(self._memory, self._batch_size)

        for current_state, action, reward, next_state, done in mini_batch:
            self._fitModel(current_state, action, reward, next_state, done)

    def _fitModel(self, current_state, action, reward, next_state, done):
        if not done:
            new_value = reward + self._gamma * np.amax(self._model.predict(next_state))
        else:
            new_value = reward

        nodes = self._model.predict(current_state)
        nodes[0][action] = new_value

        self._model.fit(current_state, nodes, epochs=1, verbose=0)

    def load(self, file):
        from keras import models  # não importar logo de primeira

        self._model = models.load_model(file)

    def save(self, file):
        self._model.save(file)
