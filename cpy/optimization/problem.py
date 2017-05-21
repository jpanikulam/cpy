import sympy
# Problem definition

# Plan:
# Minimize general cost functions
# Minimize dynamics cost functions
# Support rotation
# Write simulator


def simple_dynamics():
    x = sympy.Symbol('x')
    y = sympy.Symbol('y')
    xdot = sympy.Symbol('xdot')
    ydot = sympy.Symbol('ydot')

    u_1 = sympy.Symbol('u_1')
    u_2 = sympy.Symbol('u_2')

    q = sympy.Matrix([
        x,
        y,
        xdot,
        ydot,
    ])

    u = sympy.Matrix([
        u_1,
        u_2,
    ])

    qdot = sympy.Matrix([
        xdot,
        ydot,
        u_1,
        u_2
    ])

    dynamics = {
        'state': q,
        'control': u,
        'dynamics': qdot,
    }

    return dynamics


def vec_subs(expr, vec, targs):
    nexpr = expr
    for n, elem in enumerate(vec):
        nexpr = nexpr.subs(elem, targs[n])

    return nexpr


def rk4(dynamics):
    q = dynamics['state']
    qdot = dynamics['dynamics']

    h = sympy.Symbol('h')
    h_half = sympy.Rational(1, 2) * h
    h_sixth = sympy.Rational(1, 6) * h

    k1 = qdot
    k2 = vec_subs(qdot, q, q + (h_half * k1))
    k3 = vec_subs(qdot, q, q + (h_half * k2))
    k4 = vec_subs(qdot, q, q + (h * k3))

    qn = q + (h_sixth * h) * (k1 + (2 * k2) + (2 * k3) + k4)
    return qn


class Problem(object):
    def __init__(self):
        problem = {
            'minimize': None,
            'subject_to': None,
        }

        self.state_dimension = 4
        self.control_dimension = 2


if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt

    dyn = simple_dynamics()
    qn_f = rk4(dyn)

    xx = np.array([0.0, 0.0, 1.0, 0.0])
    qn_f = qn_f.subs(sympy.Symbol('h'), 0.1)
    qn_fixed_u = vec_subs(qn_f, dyn['control'], np.array([0.001, -0.1]))

    t = np.arange(0.0, 2.0, 0.1)
    hist = []

    for tt in t:
        xx = np.array(vec_subs(qn_fixed_u, dyn['state'], xx))
        hist.append(xx)

    hist = np.hstack(hist)
    plt.plot(t, hist[1, :])
    plt.plot(t, hist[0, :])
    # plt.show()
