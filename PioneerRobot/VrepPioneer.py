from VrepApi import vrep
from .PioneerRobot import PioneerRobot
import numpy as np
import time
from pynput.keyboard import Key, Listener
from pynput import keyboard


class VrepPioneer(PioneerRobot):
    __sensors_id = dict()
    __sensor_values = - np.ones(16)
    __left_motor_id = -1
    __right_motor_id = -1

    def __init__(self, server_ip: str, server_port: int):
        self.__client_id = vrep.simxStart(server_ip, server_port, True, True, 5000, 5)

        self._connect_all_peaces()

    def _connect_all_peaces(self):
        vrep_sensor_name = "Pioneer_p3dx_ultrasonicSensor"

        for i in range(1, 17):
            vrep_sensor_full_name = vrep_sensor_name + str(i)
            self.__sensors_id[vrep_sensor_full_name] = self._connect_peace(vrep_sensor_full_name)

        self.__left_motor_id = self._connect_peace("Pioneer_p3dx_leftMotor")
        self.__right_motor_id = self._connect_peace("Pioneer_p3dx_rightMotor")

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
                                                                                  vrep.simx_opmode_buffer)
        while status == vrep.simx_return_novalue_flag:
            status, detection_state, values, doh, dsnv = vrep.simxReadProximitySensor(self.__client_id, sensor_id,
                                                                                      vrep.simx_opmode_buffer)

        if status == vrep.simx_return_ok:
            return values[2]
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
                                                          vrep.simx_opmode_streaming)

            status_right = vrep.simxSetJointTargetVelocity(self.__client_id, self.__left_motor_id, right_motor_velocity,
                                                           vrep.simx_opmode_streaming)

    def _on_press(self, key):

        velocity = 0.3
        reduce = 0.3
        key_value = str(key)[1]

        if key_value == "w":
            self.set_velocity_motor(velocity, velocity)

        elif key_value == "s":
            self.set_velocity_motor(-velocity, -velocity)

        elif key_value == "a":
            self.set_velocity_motor(velocity * reduce, -velocity * reduce)

        elif key_value == "d":
            self.set_velocity_motor(-velocity * reduce, velocity * reduce)

    def control_the_robot(self):
        print("start Controller")
        listener = Listener(on_press=self._on_press)
        listener.start()

        # with Listener(on_press=self._on_paress) as listener:
        #     listener.run()

        dataset = list()

        while vrep.simxGetConnectionId(self.__client_id) != -1:
            value_sensors = self.get_ultrasonic_sensor_values()
            dataset.append(value_sensors)
            time.sleep(0.5)
            pass

        print("Saving Dataset")
        np.savetxt("dataset.csv", np.array(dataset), delimiter=",")

        listener.stop()
        listener.join()
