from matplotlib import pyplot as plt
import numpy as np


if __name__ == '__main__':

    plt.ion()
    for _ in range(20):
        y = np.random.random(200)
        X = np.random.random((200, 20))

        # plt.plot(y)
        plt.cla()
        # plt.plot(y)
        plt.imshow(X)
        plt.draw()
        plt.pause(0.0000001)

    plt.ioff()
