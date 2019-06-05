from VrepApi import vrep
import numpy as np
import time


class VrepPioneer:
    __sensors_id = dict()
    __sensor_values = - np.ones(16)
    __left_motor_id = -1
    __right_motor_id = -1

    def __init__(self, server_ip: str, server_port: int):
        self.__client_id = vrep.simxStart(server_ip, server_port, True, True, 5000, 5)

        self._connect_all_peaces()

    def _connect_all_peaces(self):
        vrep_sensor_name = "Pioneer_p3dx_ultrasonicSensor"

        for i in range(1, 16):
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

    def set_velocity_motor_right(self, velocity_value: float):
        status = vrep.simxSetJointTargetVelocity(self.__client_id, self.__right_motor_id, velocity_value,
                                                 vrep.simx_opmode_streaming)

        while status == vrep.simx_return_novalue_flag:
            status = vrep.simxSetJointTargetVelocity(self.__client_id, self.__right_motor_id, velocity_value,
                                                     vrep.simx_opmode_streaming)
