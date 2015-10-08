import string
from core import Code
from cpptypes import Ptr, Type, Variable


class While():
    def __init__(self, expression):
        self.condition = str(expression)

    def __enter__(self):
        Code.add('while ({})'.format(self.condition))
        Code.start_scope()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Will I ever use that kind of funny business?
        Code.end_scope()

class If(object):
    def __init__(self, expression):
        self.condition = str(expression)

    def __enter__(self):
        Code.add('if ({})'.format(self.condition))
        Code.start_scope()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Will I ever use that kind of funny business?
        Code.end_scope()


class Else(object):
    '''TODO: Make this smart
    '''
    def __enter__(self):
        Code.add('else')
        Code.start_scope()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Will I ever use that kind of funny business?
        Code.end_scope()


class ElseIf(object):
    '''TODO: Make this smart
    '''
    def __init__(self, expression):
        self.condition = str(expression)

    def __enter__(self):
        Code.add('else if ({})'.format(self.condition))
        Code.start_scope()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Will I ever use that kind of funny business?
        Code.end_scope()


if __name__ == '__main__':
    a = Variable('a', Type('int'))
    b = Variable('b=2', Type('bool'))

    a.declare()
    b.declare()

    with If((a == 1) < 1):
        Code.add_line("is()")
    with ElseIf("b"):
        Code.add_line("CPY()")
    with Else():
        Code.add_line("worth_it()")

    print Code.code
