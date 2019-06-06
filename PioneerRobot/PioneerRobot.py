from abc import ABC, abstractclassmethod
import numpy


class PioneerRobot(ABC):



    @abstractclassmethod
    def get_ultrasonic_sensor_values(self) -> numpy.array: ...

    @abstractclassmethod
    def set_velocity_motor(self, left_motor_velocity: float, right_motor_velocity: float) -> None: ...
