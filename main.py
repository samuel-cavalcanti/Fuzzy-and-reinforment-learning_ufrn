from PioneerRobot.VrepPioneer import VrepPioneer
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator
import skfuzzy as fuzz

if __name__ == '__main__':
    # robot = VrepPioneer("192.168.15.29", 19996)
    # robot.control_the_robot()
    #
    # data = np.loadtxt("dataset_right.csv", delimiter=",").T
    # new_data = np.loadtxt("dataset_left.csv", delimiter=",").T
    # cntr = np.loadtxt("centros.csv", delimiter=",")
    # all_data = np.concatenate((data, new_data), axis=1)
    # print("cntr.shape ", cntr.shape)
    #
    # #
    # # print(all_data.shape)
    # # cntr, u, _, _, _, _, fpc = fuzz.cluster.cmeans(new_data, 10, 2, error=0.0001, maxiter=1000, init=None)
    # test = np.reshape(all_data[:, 0], (-1, 1))
    # print("test", test.shape)
    # u, u0, d, jm, p, fpc = fuzz.cluster.cmeans_predict(test, cntr, 2, error = 0.0001,
    #                                                                       maxiter = 1000)
    #
    # cluster_membership = np.argmax(u, axis=0)
    # print(u)

    # fpcs = list()
    # cntrs = list()
    # final = 20
    # init = 1
    #
    # for i in range(init, final):
    #     cntr, u, _, _, _, _, fpc = fuzz.cluster.cmeans(all_data, i, 2, error=0.0001, maxiter=1000, init=None)
    #     print("it {} fpc {}".format(i, fpc))
    #     print("cntr.shape ", cntr.shape)
    #     fpcs.append(fpc)
    #     cntrs.append(cntr)
    #
    # fig2, ax2 = plt.subplots()
    # ax2.plot(np.r_[init:final], fpcs, "o")
    # ax2.set_xlabel("Number of centers")
    # ax2.set_ylabel("Fuzzy partition coefficient")
    # ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    #
    # plt.show()
    #
    # n = int(input("n states: \n"))
    #
    # np.savetxt("centros.csv", cntrs[n], delimiter=",")
