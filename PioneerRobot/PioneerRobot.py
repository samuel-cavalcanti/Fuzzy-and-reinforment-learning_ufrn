from abc import ABC, abstractclassmethod
import numpy


class PioneerRobot(ABC):

    @abstractclassmethod
    def get_ultrasonic_sensor_values(self) -> numpy.array: ...

    @abstractclassmethod
    def set_velocity_motor(self, left_motor_velocity: float, right_motor_velocity: float) -> None: ...

    @abstractclassmethod
    def random_move(self) -> int: ...

    @abstractclassmethod
    def is_connected(self) -> bool: ...

    def reset_connection(self) -> None: ...

    @abstractclassmethod
    def conect_to_robot(self) -> bool: ...

    @abstractclassmethod
    def close_connection(self): ...

    @abstractclassmethod
    def collision(self) -> bool: ...
