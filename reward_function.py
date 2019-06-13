import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Required for 3D plotting


class RewardFunction:
    __sensors = [ctrl.Antecedent(np.arange(0, 1.01, 0.01), "sensor front"),
                 ctrl.Antecedent(np.arange(0, 1.01, 0.01), "sensor right")]

    __reward = ctrl.Consequent(np.arange(-1, 1.11, 0.01), "reward")

    __delay = -1

    def __init__(self, close_sensors_points: list, good_sensors_points: list, far_sensors_points: list,
                 bad_reward_points: list, good_reward_points: list, neutral_reward_points: list):
        self._init_sensors(close_sensors_points, good_sensors_points, far_sensors_points)

        self._init_reward(bad_reward_points, good_reward_points, neutral_reward_points)

        self.__reward_function = self._config_control_system()

    def _init_sensors(self, close_points: list, good_points: list, far_points: list):

        for sensor in self.__sensors:
            sensor["close"] = fuzz.trapmf(sensor.universe, close_points)

            sensor["good"] = fuzz.trimf(sensor.universe, good_points)

            sensor["far"] = fuzz.trapmf(sensor.universe, far_points)

    def _init_reward(self, bad_points: list, good_points: list, neutral_points: list):

        # reward

        self.__reward["bad"] = fuzz.trimf(self.__reward.universe, bad_points)

        self.__reward["neutral"] = fuzz.trimf(self.__reward.universe, neutral_points)

        self.__reward["good"] = fuzz.trimf(self.__reward.universe, good_points)

    def _config_control_system(self):

        front_sensor = self.__sensors[0]

        right_sensor = self.__sensors[1]

        # bad rules

        rule0 = ctrl.Rule(front_sensor["close"] | right_sensor["close"], self.__reward["bad"])

        # good rules

        rule1 = ctrl.Rule(front_sensor["good"] & right_sensor["good"], self.__reward["good"])

        rule2 = ctrl.Rule(front_sensor["good"] & right_sensor["far"], self.__reward["good"])

        # far rules

        rule3 = ctrl.Rule(front_sensor["far"] & right_sensor["good"], self.__reward["good"])

        rule4 = ctrl.Rule(front_sensor["far"] & right_sensor["far"], self.__reward["neutral"])

        reward_ctrt = ctrl.ControlSystem([rule0, rule1, rule2, rule3, rule4])

        reward_function = ctrl.ControlSystemSimulation(reward_ctrt)

        return reward_function

    def get_reward(self, front_sensor_value: float, right_sensor_value: float):

        self.__reward_function.input["sensor right"] = right_sensor_value

        self.__reward_function.input["sensor front"] = front_sensor_value

        self.__reward_function.compute()

        if self.__delay == -2:

            self.__reward.view(sim=self.__reward_function)

            plt.show()

        elif self.__delay != -1:
            self.__reward.view(sim=self.__reward_function)
            plt.ion()
            plt.show()
            plt.pause(self.__delay)

        return round(self.__reward_function.output["reward"], 15)

    def plot_in_Real_time(self, delay: float):
        self.__delay = delay

    def plot_control_space(self):

        self.plot_in_Real_time(-1)

        upsampled = np.arange(0, 1.1, 0.1)

        x, y = np.meshgrid(upsampled, upsampled)
        z = np.zeros_like(x)

        for i in range(upsampled.size):
            for j in range(upsampled.size):
                z[i, j] = self.get_reward(x[i, j], y[i, j])

        fig = plt.figure("Surface Control", figsize=(8, 8))

        ax = fig.add_subplot(111, projection='3d')

        surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap='viridis',
                               linewidth=0.4, antialiased=True)

        cset = ax.contourf(x, y, z, zdir='z', offset=-2.5, cmap='viridis', alpha=0.5)
        cset = ax.contourf(x, y, z, zdir='x', offset=3, cmap='viridis', alpha=0.5)
        cset = ax.contourf(x, y, z, zdir='y', offset=3, cmap='viridis', alpha=0.5)

        ax.view_init(30, 200)

        plt.show()

    def plot_output(self, n_sensor: int):

        self.__sensors[n_sensor].view(sim=self.__reward_function)

        self.__reward.view(sim=self.__reward_function)

        plt.show()
