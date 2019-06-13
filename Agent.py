from model.DeepQLearning import DeepQLearning
from PioneerRobot.PioneerRobot import PioneerRobot
from reward_function import RewardFunction
import numpy as np
import time
from pynput.keyboard import Listener


class Agent:
    __data = list()

    def __init__(self, pioneer_robot: PioneerRobot, model: DeepQLearning, reward_function: RewardFunction):
        self.__robot = pioneer_robot
        self.__model = model
        self.__fuzzy_reward = reward_function

    def _move_robot(self, action: int):
        velocity = 0.3
        reduce = 0.3

        if action == 0:
            self.__robot.set_velocity_motor(velocity, velocity)
        else:  # left
            self.__robot.set_velocity_motor(velocity * reduce, -velocity * reduce)

    def _get_state(self) -> np.array:

        time.sleep(0.3)

        value_sensors = self.__robot.get_ultrasonic_sensor_values()

        front = value_sensors[3:6].mean()
        right = value_sensors[7:9].mean()

        state = np.array([front, right])

        return state.reshape((1, -1))

    def learn_by_demonstration(self, csv_file: str, mode_file: str):
        data = np.loadtxt(csv_file, delimiter=",")
        done = False
        epsodes = 100
        for j in range(epsodes):
            for i in range(len(data) - 1):
                current_state = np.reshape(data[i, 1:], (1, -1))
                next_state = np.reshape(data[i + 1, 1:], (1, -1))

                self.__model._current_state = current_state

                self.__model._current_action = int(data[i, 0])

                reward = self.__fuzzy_reward.get_reward(next_state[0][0], next_state[0][1])

                self.__model.update(next_state, reward, done, None)

        print("saving model")
        self.__model.save(mode_file)

    def learn(self, file="None"):

        steps = 0
        episodes = 0
        done = False

        self.__model.load(file)

        self.__model._epsilon = 0.01

        while self.__robot.is_connected():
            current_state = self._get_state()

            action = self.__model.action(current_state)

            self._move_robot(action)

            next_state = self._get_state()

            if next_state[0, 0] < 0 or next_state[0, 1] < 0:
                continue

            reward = self.__fuzzy_reward.get_reward(next_state[0][0], next_state[0][1])

            if steps == 200 or self.__robot.collision():  # 150
                self.__robot.reset_connection()
                steps = 0
                episodes += 1
                done = True
            if episodes == 100000:
                self.__robot.close_connection()

            print("current state {} reward {} n steps: {}".format(next_state, reward, steps))
            self.__model.update(next_state, reward, False, done)

            steps += 1
            done = False

        print("saving model")
        self.__model.save(file)

    def control_agent(self):

        print("start Controller")
        listener = Listener(on_press=self._on_press)
        listener.start()

        self.__data.clear()

        while self.__robot.is_connected():
            time.sleep(0.5)
            pass

        print("Saving DataSet")
        np.savetxt("dataset1.csv", np.array(self.__data), delimiter=",")
        print("DataSet saved")
        listener.stop()
        listener.join()

    def _on_press(self, key):

        velocity = 0.3
        reduce = 0.3
        key_value = str(key)[1]
        decision = -1

        if key_value == "w":
            self.__robot.set_velocity_motor(velocity, velocity)
            decision = 0

        elif key_value == "s":
            self.__robot.set_velocity_motor(-velocity, -velocity)

        elif key_value == "a":
            self.__robot.set_velocity_motor(velocity * reduce, -velocity * reduce)
            decision = 1

        elif key_value == "d":
            self.__robot.set_velocity_motor(-velocity * reduce, velocity * reduce)

        if decision != -1:
            state = self._get_state()
            reward = self.__fuzzy_reward.get_reward(state[0, 0], state[0, 1])

            print("decision: {} state: {} reward: {}".format(decision, state.reshape(state.size), reward))
            data = [decision, state[0, 0], state[0, 1]]
            self.__data.append(data)
