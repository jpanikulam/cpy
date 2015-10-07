import string
from core import Code

class While():
    def __init__(self, expression):
        self.condition = expression

    def __enter__(self):
        Code.add('while (self.condition)')
        Code.start_scope()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Will I ever use that kind of funny business?
        Code.end_scope()

class If(object):
    def __init__(self, expression):
        self.condition = expression

    def __enter__(self):
        Code.add('if (self.condition)')
        Code.start_scope()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Will I ever use that kind of funny business?
        Code.end_scope()

    class Else(object):
        def __enter__(self):
            Code.add('else')
            Code.start_scope()

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Will I ever use that kind of funny business?
            Code.end_scope()

    class ElseIf(object):
        def __init__(self, expression):
            self.condition = expression

        def __enter__(self):
            Code.add('else if (self.condition)')
            Code.start_scope()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Will I ever use that kind of funny business?
            Code.end_scope()


if __name__ == '__main__':
    with If('a == true') as if_1:
        Code.add_line("is()")
        with if_1.ElseIf("b"):
            Code.add_line("CPY()")
        with if_1.Else():
            Code.add_line("worth_it()")

    print Code.code