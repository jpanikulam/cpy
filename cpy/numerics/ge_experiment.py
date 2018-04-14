import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict
import itertools
import time

np.random.seed(seed=989)


def sym_set(X, a, b, v):
    X[a, b] = v
    X[b, a] = v


def draw_adjacency(adj, shape):
    image = np.zeros(shape)
    for start, dests in adj.items():
        for dest in dests:
            sym_set(image, start, dest, 1.0)

    plt.imshow(image)


def adjacency_from_sym(X):
    adjacency = defaultdict(lambda: [])
    for i in range(X.shape[0]):
        for j in range(i, X.shape[1]):
            val = X[i, j]
            if val != 0.0:
                adjacency[i].append(j)
                adjacency[j].append(i)
    return adjacency


def predict_fill_in(X):
    fill_in_predicted = np.copy(X)
    adjacency = adjacency_from_sym(X)

    # Eliminate (graphically, I mean) in order, until we have a fill-in estimate
    ANIMATE = False
    plt.ion()
    plt.figure("Estimated")
    i = 0
    while(True):
        if i not in adjacency.keys():
            break
        dests = adjacency[i]
        print adjacency
        for dest in dests:
            adjacency[dest].pop(adjacency[dest].index(i))

        adjacency.pop(i)

        if(ANIMATE):
            plt.cla()
            # draw_adjacency(adjacency, X.shape)
            Xdiag = np.diag(np.diag(X))
            plt.imshow(np.tril(fill_in_predicted + Xdiag) != 0.0, origin='upper')
            plt.draw()
            plt.pause(0.5)

        for a, b in itertools.product(dests, dests):
            if a >= b:
                fill_in_predicted[a, b] = 1.0
                fill_in_predicted[b, a] = 1.0

        fill_in_predicted[i, i] = 0.0

        adjacency = adjacency_from_sym(fill_in_predicted)
        print '---'
        # print adjacency

        i += 1

    plt.ioff()
    Xdiag = np.diag(np.diag(X))
    plt.imshow(np.tril(fill_in_predicted + Xdiag) != 0.0, origin='upper')

    # plt.show()

    # plt.figure("Predicted")
    # plt.imshow(fill_in_predicted)
    # plt.show()


def swap_cols(X, a, b):
    temp = X[:, a]
    X[:, a] = X[:, b]
    X[:, b] = temp
    return X


if __name__ == '__main__':
    # P = np.array([
    #     [0.42596851, 0.85237279, 0.42728069, 0.77173962, 0.40351419],
    #     [0.85237279, 0.09127184, 0.48072670, 0.53979327, 0.79138437],
    #     [0.42728069, 0.48072670, 0.80000000, 0.77736127, 0.47094075],
    #     [0.77173962, 0.44460465, 0.77736127, 0.53979327, 0.99930384],
    #     [0.40351419, 0.79138437, 0.44460465, 0.92769807, 0.47094075]
    # ])
    SHAPE = 10
    # P = np.random.random((SHAPE, SHAPE))
    # P = P.dot(P.transpose())
    # P[np.abs(P) < 2.5] = 0

    P = np.zeros((SHAPE, SHAPE))
    # P[0:SHAPE, 0] = np.random.random(SHAPE)
    # P[0, 0:SHAPE] = np.random.random(SHAPE)
    P[SHAPE - 1, :] = np.random.random(SHAPE)
    P[:, SHAPE - 1] = np.random.random(SHAPE)
    P += np.eye(SHAPE) * 4.0

    sym_set(P, 5, 8, 1.0)
    sym_set(P, 3, 6, 1.0)
    sym_set(P, 0, 2, 1.0)
    sym_set(P, 0, 3, 1.0)
    sym_set(P, 0, 4, 1.0)

    P += np.eye(SHAPE) * 4.0

    predict_fill_in(P)
    Pchol = np.linalg.cholesky(P)

    # plt.figure("Original")
    # plt.imshow(P != 0.0, origin='upper')
    plt.figure("Cholesky")
    plt.imshow(Pchol != 0.0, origin='upper')
    plt.show()
