from core import Code
from abstract import CpyStruct
from collections import OrderedDict


def edecl(obj, name):
    cstruct = CpyStruct(name)
    cstruct.add_members(obj)
    return cstruct


def main():
    Gains = OrderedDict([
        ('xpos', 'double'),
        ('ypos', 'double'),
        ('theta', 'double'),
        ('xdot', 'double'),
        ('ydot', 'double'),
        ('thetadot', 'double'),
        ('surge', 'double'),
        ('sway', 'double'),
        ('torque', 'double'),
    ])

    Obstacle = OrderedDict([
        ('weight', 'double'),
        ('vehicle_radius', 'double'),
    ])

    Main = OrderedDict([
        ('gains', 'Gains'),
        ('obstacle', 'Obstacle')
    ])

    code = Code()
    code.add_struct(edecl(Gains, 'Gains'))
    code.add_struct(edecl(Obstacle, 'Obstacle'))
    code.add_struct(edecl(Main, 'Main'))

    # code.generate()
    print code


if __name__ == '__main__':
    main()
