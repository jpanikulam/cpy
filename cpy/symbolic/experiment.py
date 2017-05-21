import numpy as np
from scipy import linalg as scla

from numdiff import jacobian

import sympy
import sym_utils as su

if __name__ == '__main__':

    normal = su.vector('nhat', 2)
    q = su.vector('q', 2)
    c = su.vector('c', 2)

    diff = q - c

    d = su.cross2d(normal, diff)
    sympy.pretty_print(d)
    sympy.pretty_print(su.gradient(d, q))


def skew2d(theta):
    return np.array([
        [0.0, -theta],
        [theta, 0.0],
    ])


def skewtrans(theta, t):
    r2d = skew2d(theta)
    wx = np.zeros((3, 3))
    wx[:2, :2] = r2d
    wx[0, 2] = t[0]
    wx[1, 2] = t[1]
    return wx


def exp2dwt(thetat):
    wx = skewtrans(thetat[0], thetat[1:])
    return scla.expm(wx)


def expt(x):
    T = exp2dwt(x)
    y = np.array([1.0, 1.0, 1.0])
    return T.dot(y)


if __name__ == '__main__1':
    theta = 1.6
    y = np.array([1.0, 1.0])
    t = np.array([0.0, 0.0])

    tt = np.hstack([theta, t])

    # print expt(tt)
    print jacobian(expt, tt)
    print '----'

    M = np.array([
        [np.sin(theta), -(1 - np.cos(theta))],
        [1 - np.cos(theta), np.sin(theta)],
    ])
    V = (1 / theta) * M

    vprime = np.array([
        [(np.cos(theta) / theta) - (np.sin(theta) / theta**2), (-np.sin(theta) / theta) - ((np.cos(theta) - 1) / theta**2)],
        [(np.sin(theta) / theta) - ((-np.cos(theta) + 1) / theta**2), (np.cos(theta) / theta) - (np.sin(theta) / theta**2)],
    ])

    # print V.dot(t)
    # print vprime
    theta2 = theta + (np.pi / 2.0)
    rr = np.array([
        [np.cos(theta2), -np.sin(theta2)],
        [np.sin(theta2), np.cos(theta2)]
    ])

    print 'rr'
    print rr
    print 'vprime'
    print vprime
    print 'V'
    print V
    print rr.dot(y).transpose() + vprime.dot(t)
    # print vprime.dot(t)
