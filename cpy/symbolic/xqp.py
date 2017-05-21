import sympy
from cpy.symbolic import sparse
from cpy.symbolic import sym_utils


class DisciplinedConvexProblem(object):
    """Solves a QP.

    Specified in the form:
        min_{x}: (1 / 2) quad(Q, x) + (q.T * x)
    s.t.
        Gx + s = h
        Ax = b
        (s >= 0)

    Where quad(Q, x): x.T * Q * x
    This term will be reused.
    """

    def __init__(self):
        self._x_dim = 0
        self._h_dim = 0
        self._b_dim = 0

        self._A = []
        self._G = []
        self._Q = []

        self._h_dim
        self._b_dim

        self._state_tree = {}

    def add_cost(self):
        pass

    def add_constraint(self, x_ind, min, max):
        pass

if __name__ == '__main__':

    Qlist = []
    for k in range(5):
        Qn = sym_utils.matrix('Q^({})'.format(k), (5, 5))
        Qlist.append(sym_utils.to_sparse(Qn))
        sympy.pretty_print(Qn)

    Q = sparse.diagstack(sparse.identity(5), *Qlist)
    Q.spy()
    from matplotlib import pyplot as plt
    plt.show()
