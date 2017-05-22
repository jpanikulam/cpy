import sparse  # noqa
from functools import partial


class MatrixPolicy(object):
    def __init__(self):
        pass

    def write(self, MatrixOperation):
        raise NotImplementedError

    def function_block(self):
        raise NotImplementedError


class NoOptEigenPolicy(MatrixPolicy):
    def __init__(self):
        self._op_map = {
            sparse.Product: partial(self._multi, name="*"),
            sparse.Sum: partial(self._multi, name="+"),
            sparse.Inverse: partial(self._method, name="inverse"),
            sparse.Transpose: partial(self._method, name="transpose"),
            sparse.Negate: partial(self._unary, name="-"),
            sparse.SparseMatrix: self._base,
        }

        self.members = set()

    def _stringify(self, op):
        op_func = self._op_map[type(op)]
        op_str = op_func(op)
        return op_str

    def _base(self, op):
        self.members.add(op)
        return op.name

    def _unary(self, op, name):
        op_str = self._stringify(op.mtx)
        return "{}{}".format(name, op_str)

    def _multi(self, op, name):
        ops = []
        for contributor in op.contributors:
            ops.append(self._stringify(contributor))
        op_str = " {} ".format(name).join(ops)
        return "({})".format(op_str)

    def _method(self, op, name):
        op_str = self._stringify(op.mtx)
        return "{}.{}()".format(op_str, name)

    def declare(self):
        pass

    def write(self, mat_operation):
        self.members.clear()
        text = self._stringify(mat_operation)
        self.members = set(self.members)
        return text


def implement_operation(op, policy):
    text = policy.write(op)
    return text


if __name__ == '__main__':
    v = sparse.SparseMatrix((5, 1), name="v")
    R = sparse.SparseMatrix((5, 5), name="R")
    M1 = sparse.SparseMatrix((5, 5), name="M1")
    J = sparse.SparseMatrix((5, 6), name="J")
    M3 = sparse.SparseMatrix((6, 5), name="M3")

    delta = (J.transpose() * R.inv() * J).inv() * J.transpose() * v
    policy = NoOptEigenPolicy()
    print delta
    print policy.write(delta)
