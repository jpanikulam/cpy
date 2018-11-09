import sympy

from cpy.symbolic import sparse


def vector(name, length=3):
    """Dense vector where each element has a symbol name."""
    symbols = []
    for k in range(length):
        symbols.append(
            sympy.Symbol("{}_{}".format(name, k))
        )

    return sympy.Matrix(symbols)


def matrix(name, shape):
    """Dense matrix where each element has a symbol name."""
    symbols = []
    m, n = shape
    for row in range(m):
        row_symbols = []
        for col in range(n):
            row_symbols.append(
                sympy.Symbol("{}_({}_{})".format(name, row, col))
            )
        symbols.append(row_symbols)

    return sympy.Matrix(symbols)


def norm(expr):
    """No sussing around with this "abs" business."""
    return sympy.sqrt(expr.dot(expr))


def gradient(expr, symbol):
    return sympy.Matrix([expr]).jacobian(symbol)


def rotation2d(theta):
    return sympy.Matrix([
        [sympy.cos(theta), -sympy.sin(theta)],
        [sympy.sin(theta), sympy.cos(theta)]
    ])


def cross2d(a, b):
    return (a[0] * b[1]) - (a[1] * b[0])


def to_sparse(matrix):
    entries = {}
    for row in range(matrix.rows):
        for col in range(matrix.cols):
            val = matrix[row, col]

            # Exactly uniquely zero! Not almost zero! No bullshit!
            if val != 0:
                entries[(row, col)] = val

    return sparse.SparseMatrix(matrix.shape, entries)


def vec_subs(expr, vec, targs):
    nexpr = expr
    for n, elem in enumerate(vec):
        nexpr = nexpr.subs(elem, targs[n])

    return nexpr


if __name__ == '__main__':
    a = vector('a', 5)
    b = vector('b', 5)
    sympy.pretty_print(a)

    A = matrix('A', (5, 5))
    sympy.pretty_print(A)

    sympy.pretty_print(norm(a - b))

    sA = to_sparse(A)
    sb = to_sparse(b)
    sparse.diagstack(sA, sA, sA, sA, sb).spy()

    from matplotlib import pyplot as plt
    plt.show()
