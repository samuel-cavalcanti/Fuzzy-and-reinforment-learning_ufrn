from VrepApi import vrep
from Agent import Agent
import time


class VrepEnvironment:

    def __init__(self, agent: Agent, server_ip="127.0.0.1", server_port=19996):
        self.__client_id = vrep.simxStart(server_ip, server_port, True, True, 5000, 5)
        self.__server_ip = server_ip
        self.__server_port = server_port
        self.__agent = agent

    def reset_connection(self, client_id) -> None:
        vrep.simxFinish(client_id)

        print("resetting simulation")

        vrep.simxStopSimulation(self.__client_id, vrep.simx_opmode_blocking)

        time.sleep(5)

        vrep.simxStartSimulation(self.__client_id, vrep.simx_opmode_blocking)

        time.sleep(2)

        print("simulation started")
