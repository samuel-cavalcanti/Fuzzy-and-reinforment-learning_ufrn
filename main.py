from VrepPioneer import VrepPioneer

if __name__ == '__main__':
    robot = VrepPioneer("192.168.15.29", 19997)

    robot.set_velocity_motor(1, 1)
