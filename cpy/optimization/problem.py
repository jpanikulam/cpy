import sympy
from cpy.symbolic import sparse, eigen
from dynamics import rk4

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

