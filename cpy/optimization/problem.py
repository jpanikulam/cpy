import sympy
from cpy.symbolic import sparse, eigen
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
    def __init__(self, dynamics):
        problem = {
            'minimize': None,
            'subject_to': None,
        }

        self.state_dimension = dynamics['state'].rows
        self.control_dimension = dynamics['control'].rows

    def build_iteration(self):
        A_k = sparse.SparseMatrix((self.state_dimension, self.state_dimension), name="A_k")
        B_k = sparse.SparseMatrix((self.state_dimension, self.control_dimension), name="B_k")
        R_k = sparse.SparseMatrix((self.control_dimension, self.control_dimension), name="R_k")
        P_k_next = sparse.SparseMatrix((self.state_dimension, self.state_dimension), name="P_k_next")
        Q_k = sparse.SparseMatrix((self.state_dimension, self.state_dimension), name="Q_k")

        btpa = B_k.transpose() * P_k_next * A_k
        r_plus_btpb = (R_k + (B_k.transpose() * P_k_next * B_k))
        F_k = r_plus_btpb.inv('llt') * btpa

        atpa = A_k.transpose() * P_k_next * A_k
        P_k = atpa - (btpa.transpose() * F_k) + Q_k

        print(F_k)
        print(P_k)

        print '---'
        policy = eigen.NoOptEigenPolicy()
        print policy.write(P_k)
        print policy.write(F_k)


if __name__ == '__main__':
    import numpy as np
    from matplotlib import pyplot as plt

    dyn = simple_dynamics()
    qn_f = rk4(dyn)

    p = Problem(dyn)
    p.build_iteration()

    # xx = np.array([0.0, 0.0, 1.0, 0.0])
    # qn_f = qn_f.subs(sympy.Symbol('h'), 0.1)
    # qn_fixed_u = vec_subs(qn_f, dyn['control'], np.array([0.001, -0.1]))

