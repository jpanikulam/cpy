from cpy.symbolic.sym_utils import vec_subs

import sympy


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
