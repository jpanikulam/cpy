from matplotlib import pyplot as plt
import numpy as np
import scipy.sparse
import sympy

a = sympy.Symbol('a', positive=True)
b = sympy.Symbol('b', positive=True)
c = sympy.Symbol('c', positive=True)
d = sympy.Symbol('d', positive=True)
e = sympy.Symbol('e', positive=True)

Aa = sympy.Matrix([
    [a, b, 0, 0],
    [0, a, b, 0],
    [0, 0, a, b],
    [0, 0, 0, a]
])

A = sympy.Rational(1, 2) * (Aa + Aa.transpose())

L, D  = A.LDLdecomposition()
sympy.pretty_print(L)
sympy.pretty_print(D)
sympy.pretty_print(L * D * L.transpose())

# rr = scipy.sparse.rand(10, 10, density=0.2, format='coo')
# rrcsr = scipy.sparse.coo_matrix(rr)
# plt.spy(rrcsr)
# plt.show()

# -- Build the problem out of subcosts
# -- -- Build K
# -- -- Add constraints, build (G, h), (A, b)
# --