import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator
from matplotlib import cm
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from reward_function import RewardFunction


def plot_test_n_clusters(data: np.array, init: int, final: int):
    fpcs = list()
    cntrs = list()

    for i in range(init, final):
        cntr, u, _, _, _, _, fpc = fuzz.cluster.cmeans(data, i, 2, error=0.1, maxiter=1000, init=None)
        fpcs.append(fpc)
        cntrs.append(cntr)

    fig2, ax2 = plt.subplots()
    ax2.plot(np.r_[init:final], fpcs, "o")
    ax2.set_xlabel("Number of centers")
    ax2.set_ylabel("Fuzzy partition coefficient")
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.show()


def nao_foi():
    dataset = np.loadtxt("dataset.csv", delimiter=",").T

    # plot_test_n_clusters(dataset, 2, 20)

    centroids, u, _, _, _, _, fpc = fuzz.cluster.cmeans(dataset, 5, 2, error=0.1, maxiter=1000, init=None)

    # np.savetxt("centroids.csv", centroids, delimiter=",")
    #
    # centroids = np.loadtxt("centroids.csv", delimiter=",")

    u, _, _, _, _, fpc = fuzz.cluster.cmeans_predict(dataset, centroids, 2, error=0.1, maxiter=1000, init=None)
    print("centroids shape", centroids.shape)

    print("u shape", u.shape)

    cluster_membership = np.argmax(u, axis=0)

    print(u[:, 0:1])
    print(cluster_membership)

    print(np.argmax(u[:, 0:1]))


def plot_fuzzy_functions(x: np.array, close: np.array, good: np.array, far: np.array, labels: list):
    fig, ax = plt.subplots()

    ax.plot(x, close, "r")
    ax.plot(x, good, "g")
    ax.plot(x, far, "b")

    ax.set_ylabel("Fuzzy membership")
    ax.set_xlabel("sensor")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    ax.legend(labels)
    plt.show()


def aggMemberFunc(sensor_front: float, sensor_left: float, close: np.array, good: np.array, far: np.array,
                  bad_reward: np.array, good_reward: np.array, neutral_reward: np.array) -> float:
    x = np.arange(0, 1.01, 0.01)

    # interpolar as variavels

    close_front = fuzz.interp_membership(x, close, sensor_front)
    good_front = fuzz.interp_membership(x, good, sensor_front)
    far_front = fuzz.interp_membership(x, far, sensor_front)

    close_left = fuzz.interp_membership(x, close, sensor_left)
    good_left = fuzz.interp_membership(x, good, sensor_left)
    far_left = fuzz.interp_membership(x, far, sensor_left)

    # determinar os peosos para cada antecedente

    rule0 = np.fmax(close_front, close_left)
    rule1 = np.fmax(close_front, good_left)
    rule2 = np.fmax(close_front, far_left)

    rule3 = np.fmax(good_front, close_left)
    rule4 = np.fmax(good_front, good_left)
    rule5 = np.fmax(good_front, far_left)

    rule6 = np.fmax(far_front, close_left)
    rule7 = np.fmax(far_front, good_left)
    rule8 = np.fmax(far_front, far_left)

    reward0 = rule0 * bad_reward
    reward1 = rule1 * bad_reward
    reward2 = rule2 * bad_reward

    reward3 = rule3 * bad_reward
    reward4 = rule4 * good_reward
    reward5 = rule5 * good_reward

    reward6 = rule6 * bad_reward
    reward7 = rule7 * good_reward
    reward8 = rule8 * neutral_reward

    return np.fmax(reward0, np.fmax(reward1, np.fmax(reward2, np.fmax(reward3, np.fmax(reward4, np.fmax(reward5,
                                                                                                        np.fmax(reward6,
                                                                                                                np.fmax(
                                                                                                                    reward7,
                                                                                                                    reward8))))))))


def plotsurface(close: np.array, good: np.array, far: np.array, bad_reward: np.array, good_reward: np.array,
                neutral_reward: np.array):
    sensors = np.arange(0, 1.01, 0.01)

    reward_arange = np.arange(-1, 1.01, 0.01)

    reward = np.zeros((sensors.size, sensors.size))

    for i, sensor_front in enumerate(sensors):
        for j, sensor_left in enumerate(sensors):
            ag_func = aggMemberFunc(sensor_front, sensor_left, close, good, far, bad_reward, good_reward,
                                    neutral_reward)
            reward[i, j] = fuzz.defuzz(reward_arange, ag_func, "centroid")

    fig = plt.figure("desfuzzy")
    ax = fig.gca(projection="3d")

    X, Y = np.meshgrid(sensors, sensors)

    ax.plot_surface(X, Y, reward, rstride=1, cstride=1, linewidth=0, antialiased=False)
    plt.show()


def old():
    x = np.arange(0, 1.01, 0.01)
    sigma = 0.3
    close = fuzz.gaussmf(x, 0, sigma)

    good = fuzz.gaussmf(x, 0.5, 0.2)

    far = fuzz.gaussmf(x, 1, sigma)

    # plot_fuzzy_functions(x, close, good, far, ["close", "good", "far"])

    good_reward = fuzz.trimf(x, [0.3, 0.5, 0.7])

    neutral_reward = fuzz.trimf(x, [0.7, 0.9, 1.1])

    bad_reward = fuzz.gaussmf(x, 0, 0.3)

    # plot_fuzzy_functions(x, bad_reward, good_reward, neutral_reward, ["bad", "good", "neutral"])

    # plotsurface(close, good, far, bad_reward, good_reward, neutral_reward)


# https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_tipping_problem_newapi.html#example-plot-tipping-problem-newapi-py


def works():
    sensor_left = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "sensor left")
    sensor_front = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "sensor front")
    reward = ctrl.Consequent(np.arange(-1, 1.11, 0.01), "reward")

    # left sensor

    # left sensor

    close_points = [-1.2, 0, 0.2, 0.4]

    good_points = [0.3, 0.5, 0.7]

    far_points = [0.5, 0.8, 1, 1.2]

    sensor_left["close"] = fuzz.trapmf(sensor_left.universe, close_points)

    sensor_left["good"] = fuzz.trimf(sensor_left.universe, good_points)

    sensor_left["far"] = fuzz.trapmf(sensor_left.universe, far_points)

    # front sensor

    sensor_front["close"] = fuzz.trapmf(sensor_front.universe, close_points)

    sensor_front["good"] = fuzz.trimf(sensor_front.universe, good_points)

    sensor_front["far"] = fuzz.trapmf(sensor_front.universe, far_points)

    # reward

    reward["bad"] = fuzz.trimf(reward.universe, [-1, -1, 0])

    reward["neutral"] = fuzz.trimf(reward.universe, [-0.5, 0, 0.5])

    reward["good"] = fuzz.trimf(reward.universe, [0, 1, 1])

    # bad rules

    rule0 = ctrl.Rule(sensor_front["close"] | sensor_left["close"], reward["bad"])

    # good rules

    rule1 = ctrl.Rule(sensor_front["good"] & sensor_left["good"], reward["good"])

    rule2 = ctrl.Rule(sensor_front["good"] & sensor_left["far"], reward["good"])

    # far rules

    rule3 = ctrl.Rule(sensor_front["far"] & sensor_left["good"], reward["good"])

    rule4 = ctrl.Rule(sensor_front["far"] & sensor_left["far"], reward["neutral"])

    reward_ctrt = ctrl.ControlSystem([rule0, rule1, rule2, rule3, rule4])

    reward_function = ctrl.ControlSystemSimulation(reward_ctrt)

    reward_function.input["sensor left"] = 0.4

    reward_function.input["sensor front"] = 0.7

    reward_function.compute()

    print(round(reward_function.output["reward"], 15))

    reward.view(sim=reward_function)

    plt.ion()

    plt.show()

    print("oi")

    plt.pause(1)


if __name__ == '__main__':
    # nao_foi()

    close_points = [-1.2, 0, 0.2, 0.3]

    good_points = [0.2, 0.4, 0.7]

    far_points = [0.6, 0.8, 1, 1.2]

    bad_points = [-1, -1, 0]

    neutral_points = [-0.5, 0, 0.5]

    good_reward_points = [0, 1, 1.2]

    reward_function = RewardFunction(close_points, good_points, far_points, bad_points, good_reward_points,
                                     neutral_points)

    # reward_function.plot_in_Real_time(-2)

    left_sensor_value = 0.9

    front_sensor_value = 0.7

    # reward = reward_function.get_reward(left_sensor_value, front_sensor_value)

    # print(reward)

    reward_function.plot_output(0)



    reward_function.plot_control_space()