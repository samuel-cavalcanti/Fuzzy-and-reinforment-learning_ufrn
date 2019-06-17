from VrepApi import vrep
from .PioneerRobot import PioneerRobot
import numpy as np
import time


class VrepPioneer(PioneerRobot):
    __sensors_id = dict()
    __sensor_values = - np.ones(16)
    __left_motor_id = -1
    __right_motor_id = -1
    __body = -1
    __data = list()

    def __init__(self, server_ip: str, server_port: int):
        self.__client_id = vrep.simxStart(server_ip, server_port, True, True, 5000, 5)
        self.__server_ip = server_ip
        self.__server_port = server_port

        self._connect_all_peaces()

    def _connect_all_peaces(self):
        vrep_sensor_name = "Pioneer_p3dx_ultrasonicSensor"

        for i in range(1, 17):
            vrep_sensor_full_name = vrep_sensor_name + str(i)
            self.__sensors_id[vrep_sensor_full_name] = self._connect_peace(vrep_sensor_full_name)

        self.__left_motor_id = self._connect_peace("Pioneer_p3dx_leftMotor")
        self.__right_motor_id = self._connect_peace("Pioneer_p3dx_rightMotor")
        self.__body = self._connect_peace("Pioneer_p3dx_visible")
        self.__wall = self._connect_peace("Parede")
        self.__collision = self._get_collision()

    def _connect_peace(self, vrep_name: str) -> int:

        status, piece = vrep.simxGetObjectHandle(self.__client_id, vrep_name, vrep.simx_opmode_blocking)

        if status == vrep.simx_return_ok:
            print("conectado ao " + vrep_name)
            return piece
        else:
            print(vrep_name + " não conectado")
            return status

    def _get_ultrasonic_sensor_value(self, sensor_id: int) -> float:

        vrep.simxReadProximitySensor(self.__client_id, sensor_id, vrep.simx_opmode_streaming)

        status, detection_state, values, doh, dsnv = vrep.simxReadProximitySensor(self.__client_id, sensor_id,
                                                                                  vrep.simx_opmode_oneshot)
        while status == vrep.simx_return_novalue_flag and self.is_connected():
            status, detection_state, values, doh, dsnv = vrep.simxReadProximitySensor(self.__client_id, sensor_id,
                                                                                      vrep.simx_opmode_buffer)

        if status == vrep.simx_return_ok:

            if detection_state:
                return values[2]

            else:
                return 1
        else:
            return -1.0

    def _get_ultrasonic_sensor_values(self):

        for i, sensor_id in enumerate(list(self.__sensors_id.values())):
            self.__sensor_values[i] = self._get_ultrasonic_sensor_value(sensor_id)

    def get_ultrasonic_sensor_values(self) -> np.array:
        self._get_ultrasonic_sensor_values()
        return self.__sensor_values

    def set_velocity_motor(self, left_motor_velocity, right_motor_velocity):

        self._set_velocity_motor(left_motor_velocity, right_motor_velocity)
        time.sleep(1)
        self._set_velocity_motor(0, 0)

    def _set_velocity_motor(self, left_motor_velocity, right_motor_velocity):

        status_left = vrep.simxSetJointTargetVelocity(self.__client_id, self.__right_motor_id, left_motor_velocity,
                                                      vrep.simx_opmode_streaming)

        status_right = vrep.simxSetJointTargetVelocity(self.__client_id, self.__left_motor_id, right_motor_velocity,
                                                       vrep.simx_opmode_streaming)

        while status_left == vrep.simx_return_novalue_flag or status_right == vrep.simx_return_novalue_flag:
            status_left = vrep.simxSetJointTargetVelocity(self.__client_id, self.__right_motor_id, left_motor_velocity,
                                                          vrep.simx_opmode_buffer)

            status_right = vrep.simxSetJointTargetVelocity(self.__client_id, self.__left_motor_id, right_motor_velocity,
                                                           vrep.simx_opmode_buffer)

            if self.is_connected() is False:
                break

    def random_move(self) -> int:
        sensors = self.get_ultrasonic_sensor_values()

        if np.sum(sensors[0:6]) == 6:
            return 0

        return np.random.randint(0, 1)

    def is_connected(self) -> bool:
        return vrep.simxGetConnectionId(self.__client_id) != -1

    def reset_connection(self) -> None:

        self.close_connection()

        client_id = vrep.simxStart(self.__server_ip, 19997, True, True, 5000, 5)

        print("resetting simulation")

        vrep.simxStopSimulation(client_id, vrep.simx_opmode_blocking)

        time.sleep(5)

        vrep.simxStartSimulation(client_id, vrep.simx_opmode_blocking)

        time.sleep(2)

        vrep.simxFinish(client_id)

        print("simulation started")

        self.conect_to_robot()

        self._connect_all_peaces()

    def conect_to_robot(self) -> bool:
        self.__client_id = vrep.simxStart(self.__server_ip, self.__server_port, True, True, 5000, 5)

        return self.__client_id != -1

    def close_connection(self):
        vrep.simxFinish(self.__client_id)

    def _get_collision(self) -> bool:
        status, colision = vrep.simxGetCollisionHandle(self.__client_id, "robot",
                                                       vrep.simx_opmode_blocking)

        while status == vrep.simx_return_novalue_flag:
            status, colision = vrep.simxGetCollisionHandle(self.__client_id, "robot",
                                                           vrep.simx_opmode_blocking)

        return colision

    def collision(self) -> bool:

        status, collision_status = vrep.simxReadCollision(self.__client_id, self.__collision,
                                                          vrep.simx_opmode_streaming)

        print("status", status, "collision_status", collision_status)

        while status == vrep.simx_return_novalue_flag:
            status, collision_status = vrep.simxReadCollision(self.__client_id, self.__collision,
                                                              vrep.simx_opmode_streaming)

        return collision_status
