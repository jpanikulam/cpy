import cpy2
import sympy
import unittest


class TestCpyAbstract(unittest.TestCase):

    def test_declare_simple_var(self):
        variable = cpy2.CpyVar('double', 'internet', 0.0, qualifiers=['const'])
        expected = 'double const internet = 0.0;'

        declaration = variable.declare()
        self.assertEqual(declaration, expected)

    def test_func_def(self):
        x = sympy.Symbol('x')
        y = sympy.Symbol('y')
        theta = sympy.Symbol('theta')
        xdot = sympy.Symbol('xdot')
        ydot = sympy.Symbol('ydot')
        thetadot = sympy.Symbol('thetadot')
        thrust = sympy.Symbol('thrust')
        s = sympy.sin(theta)
        c = sympy.cos(theta)
        R = sympy.Matrix([
            [c, -s],
            [s, c]
        ])

        x_body = sympy.Matrix([1.0, 0.0])
        x_world = R * x_body
        thrust_world = x_world * thrust
        q = sympy.Matrix([
            x,
            y,
            theta,
            xdot,
            ydot,
            thetadot
        ])
        qdot = sympy.Matrix([
            xdot,
            ydot,
            thetadot,
            thrust_world[0],
            thrust_world[1],
            0.0
        ])

        arg_x = cpy2.CpyVar('State', 'x', qualifiers=['const'], is_ref=True)
        arg_u = cpy2.CpyVar('Control', 'u', qualifiers=['const'], is_ref=True)

        code = cpy2.CpyScope()
        code.start()

        with cpy2.CpyFunction(
            'State const',
            'qdot',
            args=[arg_x, arg_u],
            qualifiers=['const', 'override'],
            enclosing_scope=code
        ) as func:

            func.write(cpy2.declare_const_entrants(q, 'x'))
            func.write(cpy2.eigen_vector(qdot, 'xdot'))
            func.line(['return', 'xdot'])

        code.end()
        got = code.code
        expected = ("namespace cpy_generated{State const qdot ( State const &x, Control const &u ) " +
                    "const override;{double const x = x(0);double const y = x(1);double const theta " +
                    "= x(2);double const xdot = x(3);double const ydot = x(4);double const thetadot = " +
                    "x(5);EigVector<6> xdot;xdot(0) = xdot;xdot(1) = ydot;xdot(2) = thetadot;xdot(3) = " +
                    "1.0*thrust*cos(theta);xdot(4) = 1.0*thrust*sin(theta);xdot(5) = 0.0;return xdot;}}")
        self.assertEqual(expected, got)

    def test_namespace(self):
        print
        x = cpy2.CpyVar('State', 'x', qualifiers=['const'], is_ref=True)
        code = cpy2.CpyScope()
        code.start()
        code.write(x.declaration())
        code.end()

        expected = 'namespace cpy_generated{State const &x}'
        got = code.code
        self.assertEqual(got, expected)


if __name__ == '__main__':
    unittest.main()
