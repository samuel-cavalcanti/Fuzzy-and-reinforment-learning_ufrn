from model import DeepQLearning
from PioneerRobot import PioneerRobot


class Agent:

    def __init__(self, pioneer_robot: PioneerRobot, model: DeepQLearning):
        self.__robot = pioneer_robot
        self.__model = model
